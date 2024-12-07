###############################################################################
#
# (C) Copyright 2024 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
import os
from subprocess import run as command, PIPE, DEVNULL
from types import TracebackType

from paramiko import SFTPClient, SFTPAttributes, SSHClient
from everysk.core.datetime import Date, DateTime
from everysk.core.object import BaseObject
from everysk.core.redis import RedisCacheCompressed


class KnownHosts(BaseObject):
    _cache: RedisCacheCompressed = RedisCacheCompressed()
    _cache_key: str = 'everysk-lib-sftp-known-hosts'
    _known_hosts: dict[str, str] = {}
    _home_dir: str = os.path.expanduser('~')
    _ssh_dir: str = '.ssh'
    _file: str = 'known_hosts'

    @property
    def known_hosts(self) -> dict[str, str]:
        """
        Get the known_hosts from the cache and update the local file
        """
        if not KnownHosts._known_hosts:
            known_hosts = self._cache.get(self._cache_key)
            # For the first time, cache will be empty
            if known_hosts:
                KnownHosts._known_hosts = known_hosts

                # Populate the known_hosts in the local file
                self.write()

        return KnownHosts._known_hosts

    def _get_known_hosts_file(self) -> str:
        """
        Get the known_hosts file full path.
        """
        return os.path.join(self._home_dir, self._ssh_dir, self._file)

    def add(self, hostname: str) -> None:
        """
        Add the hostname to the known_hosts in the cache and local file.

        Args:
            hostname (str): The hostname to add to the known_hosts. Example: 'files.example.com'
        """
        # Use the ssh-keyscan to get the key of the hostname
        result = command(['ssh-keyscan', hostname], stdout=PIPE, check=False, stderr=DEVNULL)
        # Add the key to the known_hosts locally
        self.known_hosts[hostname] = result.stdout.decode('utf-8')
        # Save the known_hosts to cache for future use
        self._cache.set(self._cache_key, self.known_hosts)
        # Save the known_hosts to the local file
        self.write()

    def check(self, hostname: str) -> bool:
        """
        Check if the hostname is already in the known_hosts.

        Args:
            hostname (str): The hostname to check in the known_hosts. Example: 'files.example.com'
        """
        return hostname in self.known_hosts

    def clear(self) -> None:
        """
        Clear the known_hosts from the cache and local file.
        """
        self._cache.delete(self._cache_key)
        KnownHosts._known_hosts = {}
        self.write()

    def write(self) -> None:
        """
        Write the known_hosts to the local file $HOME/.ssh/known_hosts for future use.
        """
        filename = self._get_known_hosts_file()
        # If the directory does not exist we need to create it
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'w', encoding='utf-8') as fd:
            fd.writelines(self.known_hosts.values())


class SFTP(BaseObject):
    """
    SFTP class to connect to the SFTP server.
    We could use the context manager to automatically close the connection when the object is deleted/destroyed.

    Args:
        compress (bool): If the connection will transfer compressed data. Defaults to True.
        date (Date, DateTime): The date/datetime used to parse the name. Defaults to today.
        hostname (str): The hostname of the SFTP server. Defaults to None.
        password (str): The password of the SFTP server. Defaults to None.
        port (int): The port of the SFTP server. Defaults to 22.
        timeout (int): The timeout of the SFTP connection. Defaults to 60.
        username (str): The username of the SFTP server. Defaults to None.

    Example:

        >>> from everysk.core.sftp import SFTP
        >>> with SFTP(username='', password='', hostname='') as sftp:
        ...     filename = sftp.search_by_last_modification_time(path='/dir', prefix='file_')
        >>> print(filename)
        /dir/2024/11/13/file_11.12.2024.csv
    """
    ## Private attributes
    _client: SFTPClient = None

    ## Public attributes
    compress: bool = True
    date: Date | DateTime = None
    hostname: str = None
    password: str = None
    port: int = 22
    timeout: int = 60
    username: str = None

    @property
    def client(self) -> SFTPClient:
        """
        Get the SFTP client to connect to the SFTP server.
        """
        if self._client is None:
            self._client = self.get_sftp_client(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                compress=self.compress,
                timeout=self.timeout
            )

        return self._client

    ## Private methods
    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 22,
        date: Date | DateTime = None,
        compress: bool = True,
        timeout: int = 60,
        **kwargs
    ):
        """
        Constructor to initialize the SFTP connection.

        Args:
            hostname (str, optional): The hostname of the SFTP server. Defaults to None.
            username (str, optional): The username of the SFTP server. Defaults to None.
            password (str, optional): The password of the SFTP server. Defaults to None.
            port (int, optional): The port of the SFTP server. Defaults to 22.
            date (Date, DateTime, optional): The date/datetime used to parse the name. Defaults to today.
            compress (bool, optional): If the connection will transfer compressed data. Defaults to True.
            timeout (int, optional): The timeout of the SFTP connection. Defaults to 60.
        """
        if date is None:
            date = Date.today()

        super().__init__(
            compress=compress,
            date=date,
            hostname=hostname,
            password=password,
            port=port,
            timeout=timeout,
            username=username,
            **kwargs
        )

    def __del__(self):
        """
        Destructor to close the SFTP connection when the object is deleted/destroyed.
        """
        try:
            if self._client is not None:
                # Close the SFTP connection when the object is deleted/destroyed
                self._client.close()
        except Exception: # pylint: disable=broad-except
            pass

    def __enter__(self):
        """
        Enter the context manager to return the object itself.
        """
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None):
        """
        https://docs.python.org/3/library/stdtypes.html#contextmanager.__exit__

        Returns:
            bool | None: If return is False any exception will be raised.
        """
        try:
            if self._client is not None:
                # Close the SFTP connection
                self._client.close()
                # Reset the SFTP client
                self._client = None
        except Exception: # pylint: disable=broad-except
            pass

    def sort(self, lst: list, attr: str, reverse: bool = False) -> list:
        """
        Sort the list of objects by the attribute with order by asc or desc.
        If the attribute is not found, the list will be returned as is.
        If reverse is True, the list will be sorted in descending order.

        Args:
            lst (list): The list of objects to sort.
            attr (str): The name of the attribute to sort.
            reverse (bool, optional): The final order of the list. Defaults to False.
        """
        return sorted(lst, key=lambda obj: getattr(obj, attr), reverse=reverse)

    ## Public methods
    def get_sftp_client(self, hostname: str, port: int, username: str, password: str, compress: bool, timeout: int) -> SFTPClient:
        """
        Connect to the SFTP server and return the SFTP client.

        Args:
            hostname (str): The hostname of the SFTP server.
            port (int): The port of the SFTP server.
            username (str): The username of the SFTP server.
            password (str): The password of the SFTP server.
            compress (bool): If the connection will transfer compressed data.
            timeout (int): The timeout of the SFTP connection.
        """
        ssh = SSHClient()
        known_hosts = KnownHosts()
        # Check if the hostname is already known
        if not known_hosts.check(hostname):
            # Add the hostname to the known_hosts and write to the local file
            known_hosts.add(hostname)
        # Load the known_hosts file $HOME/.ssh/known_hosts
        ssh.load_system_host_keys()
        ssh.connect(hostname=hostname, port=port, username=username, password=password, compress=compress, timeout=timeout)
        return ssh.open_sftp()

    def get_file(self, filename: str) -> bytes | None:
        """
        Get the file content from the SFTP server.
        If the file is not found, return None.
        If the filename has a date format, it will be parsed with the date attribute.
        Example: '/dir/%Y/file_%Y.csv' -> '/dir/2024/file_2024.csv'

        Args:
            filename (str): The filename with the path to get the content. Example: '/dir/2024/file_2024.csv'
        """
        if '%' in filename:
            filename = self.parse_date(filename, self.date)

        try:
            with self.client.open(filename, 'rb') as fd:
                return fd.read()
        except IOError:
            # If the file is not found, return None
            pass

        return None

    def search_by_last_modification_time(self, path: str, prefix: str) -> str | None:
        """
        Search the file by the last modification time with the prefix in the path recursively.
        If the file is not found, return None.
        If the path or prefix has a date format, it will be parsed with the date attribute.
        Example: '/dir/%Y' -> '/dir/2024' or 'file_%m.%d.%Y' -> 'file_11.30.2024'

        Args:
            path (str): The path to start search the file.
            prefix (str): The prefix of the file to search. Example: 'file_' or 'file_%m.%d.%Y'
        """
        if '%' in prefix:
            prefix = self.parse_date(prefix, self.date)
        if '%' in path:
            path = self.parse_date(path, self.date)

        objs: list[SFTPAttributes] = self.client.listdir_attr(path)
        objs = self.sort(objs, 'st_mtime', reverse=True)
        for file in objs:
            if file.filename.startswith(prefix):
                return f'{path}/{file.filename}'

            if file.longname.startswith('d'):
                result = self.search_by_last_modification_time(f'{path}/{file.filename}', prefix)
                if result:
                    return result

        return None

    def parse_date(self, name: str, date: Date) -> str:
        """
        Parse the date format in the name with the date attribute.
        Example: '/dir/%Y/file_%Y.csv' -> '/dir/2024/file_2024.csv'

        Args:
            name (str): The name with the date format to parse.
            date (Date): The date to parse the date format.
        """
        if '%' in name:
            index = name.find('%')
            date_format = name[index:index + 2]
            result = date.strftime(date_format)
            name = name.replace(date_format, result)
            if '%' in name:
                return self.parse_date(name, date)

        return name
