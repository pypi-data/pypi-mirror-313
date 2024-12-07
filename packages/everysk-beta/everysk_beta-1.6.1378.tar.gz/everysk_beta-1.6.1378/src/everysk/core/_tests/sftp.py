###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# pylint: disable=protected-access
from everysk.core import sftp
from everysk.core.datetime import Date
from everysk.core.object import BaseDict
from everysk.core.unittests import TestCase, mock


class KnownHostsTestCase(TestCase):

    def setUp(self):
        sftp.KnownHosts().clear()

    def tearDown(self) -> None:
        sftp.KnownHosts().clear()

    def test_get_known_hosts_file(self):
        hosts = sftp.KnownHosts()
        self.assertEqual(hosts._get_known_hosts_file(), '/root/.ssh/known_hosts')

    def test_know_hosts(self):
        hosts = sftp.KnownHosts()
        self.assertDictEqual(hosts.known_hosts, {})
        with open(hosts._get_known_hosts_file(), 'rb') as fd:
            result = fd.read()
            self.assertEqual(result, b'')

    def test_known_hosts_cache(self):
        sftp.KnownHosts._cache.set(sftp.KnownHosts._cache_key, {'files.everysk.com': 'files.everysk.com rsa XXXXXXX'})
        hosts = sftp.KnownHosts()
        self.assertDictEqual(hosts.known_hosts, {'files.everysk.com': 'files.everysk.com rsa XXXXXXX'})
        with open(hosts._get_known_hosts_file(), 'rb') as fd:
            result = fd.read()
            self.assertEqual(result, b'files.everysk.com rsa XXXXXXX')

    @mock.patch.object(sftp, 'command')
    def test_add(self, command: mock.MagicMock):
        command.return_value.stdout.decode.return_value = 'files.everysk.com rsa BBBBBB'
        hosts = sftp.KnownHosts()
        hosts.add('files.everysk.com')
        self.assertDictEqual(hosts.known_hosts, {'files.everysk.com': 'files.everysk.com rsa BBBBBB'})
        command.assert_called_once_with(['ssh-keyscan', 'files.everysk.com'], stdout=-1, check=False, stderr=-3)
        command.return_value.stdout.decode.assert_called_once_with('utf-8')
        with open(hosts._get_known_hosts_file(), 'rb') as fd:
            result = fd.read()
            self.assertEqual(result, b'files.everysk.com rsa BBBBBB')

    def test_check(self):
        hosts = sftp.KnownHosts()
        hosts.known_hosts['files.everysk.com'] = 'files.everysk.com rsa AAAAAA'
        self.assertTrue(hosts.check('files.everysk.com'))
        self.assertFalse(hosts.check('sftp.everysk.com'))


class SFTPTestCase(TestCase):

    def setUp(self) -> None:
        self.mock_client = mock.MagicMock(spec=sftp.SFTPClient)
        self.obj: sftp.SFTP = sftp.SFTP(
            hostname='files.everysk.com',
            port=2020,
            username='root',
            password='password',
            date=Date(2024, 11, 1),
            _client=self.mock_client
        )

    def test_del(self):
        self.obj.__del__()
        self.mock_client.close.assert_called_once_with()

    def test_enter_exit(self):
        with self.obj as sftp_client:
            self.assertEqual(sftp_client, self.obj)
        self.mock_client.close.assert_called_once_with()
        self.assertIsNone(self.obj._client)

    def test_sort(self):
        self.assertEqual(
            self.obj.sort([BaseDict(name='file1'), BaseDict(name='file3'), BaseDict(name='file2')], 'name'),
            [BaseDict(name='file1'), BaseDict(name='file2'), BaseDict(name='file3')]
        )

    def test_sort_reverse(self):
        self.assertEqual(
            self.obj.sort([BaseDict(name='file1'), BaseDict(name='file3'), BaseDict(name='file2')], 'name', reverse=True),
            [BaseDict(name='file3'), BaseDict(name='file2'), BaseDict(name='file1')]
        )

    def test_get_file(self):
        result = self.obj.get_file('file.csv')
        self.mock_client.open.assert_called_once_with('file.csv', 'rb')
        self.assertEqual(result, self.mock_client.open.return_value.__enter__.return_value.read.return_value)

    def test_get_file_with_date(self):
        result = self.obj.get_file('file_%Y-%b-%d.csv')
        self.mock_client.open.assert_called_once_with('file_2024-Nov-01.csv', 'rb')
        self.assertEqual(result, self.mock_client.open.return_value.__enter__.return_value.read.return_value)

    def test_parse_date(self):
        self.assertEqual(
            self.obj.parse_date('file_%Y-%b-%d.csv', Date(2024, 11, 1)),
            'file_2024-Nov-01.csv'
        )

    @mock.patch.object(sftp, 'command')
    @mock.patch.object(sftp, 'SSHClient')
    def test_get_sftp_client(self, client: mock.MagicMock, command: mock.MagicMock):
        sftp.KnownHosts().clear()
        command.return_value.stdout.decode.return_value = 'files.everysk.com rsa BBBBBB'
        result = self.obj.get_sftp_client('files.everysk.com', 2020, 'root', 'password', True, 60)
        command.assert_has_calls([
            mock.call(['ssh-keyscan', 'files.everysk.com'], stdout=-1, check=False, stderr=-3),
            mock.call().stdout.decode('utf-8')
        ])
        client.assert_has_calls([
            mock.call(),
            mock.call().load_system_host_keys(),
            mock.call().connect(hostname='files.everysk.com', port=2020, username='root', password='password', compress=True, timeout=60),
            mock.call().open_sftp()
        ])
        self.assertEqual(result, client.return_value.open_sftp.return_value)
        # Clear known hosts
        sftp.KnownHosts().clear()

    def test_search_by_last_modification_time(self):
        self.mock_client.listdir_attr.return_value = [
            mock.MagicMock(filename='dir01', st_mtime=1000, longname='drwxrwxrwx '),
            mock.MagicMock(filename='dir02', st_mtime=2000, longname='drwxrwxrwx '),
            mock.MagicMock(filename='file.csv', st_mtime=3000, longname='rwxrwxrwx '),
            mock.MagicMock(filename='file2.csv', st_mtime=2000, longname='rwxrwxrwx ')
        ]
        result = self.obj.search_by_last_modification_time('/dir00', 'file')
        self.assertEqual(result, '/dir00/file.csv')

    def test_search_by_last_modification_time_date(self):
        self.mock_client.listdir_attr.return_value = [
            mock.MagicMock(filename='dir01', st_mtime=1000, longname='drwxrwxrwx '),
            mock.MagicMock(filename='dir02', st_mtime=2000, longname='drwxrwxrwx '),
            mock.MagicMock(filename='file_01_11_2024.csv', st_mtime=3000, longname='rwxrwxrwx '),
            mock.MagicMock(filename='file_02_11_2024.csv', st_mtime=4000, longname='rwxrwxrwx ')
        ]
        result = self.obj.search_by_last_modification_time('/dir00', 'file_%d_%m_%Y')
        self.assertEqual(result, '/dir00/file_01_11_2024.csv')

    def test_search_by_last_modification_time_not_found(self):
        self.mock_client.listdir_attr.return_value = [
            mock.MagicMock(filename='file.csv', st_mtime=3000, longname='rwxrwxrwx '),
            mock.MagicMock(filename='file2.csv', st_mtime=2000, longname='rwxrwxrwx ')
        ]
        result = self.obj.search_by_last_modification_time('/dir00', 'file3')
        self.assertIsNone(result)

    def test_search_by_last_modification_time_recursive(self):
        self.mock_client.listdir_attr.side_effect = [
            [
                mock.MagicMock(filename='dir01', st_mtime=1000, longname='drwxrwxrwx ')
            ],
            [
                mock.MagicMock(filename='dir011', st_mtime=4000, longname='drwxrwxrwx ')
            ],
            [
                mock.MagicMock(filename='file1.csv', st_mtime=5000, longname='rwxrwxrwx ')
            ]
        ]
        result = self.obj.search_by_last_modification_time('/dir00', 'file1')
        self.assertEqual(result, '/dir00/dir01/dir011/file1.csv')
