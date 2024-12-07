###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# pylint: disable=protected-access
from concurrent import futures
from contextvars import ContextVar
from time import sleep
from everysk.core import threads
from everysk.core.datetime import DateTime
from everysk.core.unittests import TestCase, mock


user = ContextVar('username', default='default_user')
def fake_func_context_var():
    return user.get()

def div(v1: int, v2: int) -> int:
    sleep(0.1)
    return v1 / v2

class ThreadTestCase(TestCase):

    def test_results(self):
        results = []
        t1 = threads.Thread(target=div, args=(1, 2))
        t2 = threads.Thread(target=div, args=(1, 4))
        t1.start()
        t2.start()
        results = [t1.join(), t2.join()]
        self.assertEqual(len(results), 2)
        self.assertIn(0.25, results)
        self.assertIn(0.5, results)

    @mock.patch.object(threads, 'log')
    def test_error(self, log: mock.MagicMock):
        t1 = threads.Thread(target=div, args=(1, 0))
        t1.start()
        t1.join()
        log.error.assert_called_once_with(
            'Thread execution error -> target: %s, args: %s, kwargs: %s, traceback: %s',
            div,
            (1, 0),
            {},
            f'Traceback (most recent call last):\n  File "{threads.__file__}", line 180, in wait\n    self.results.append(future.result())\n                        ^^^^^^^^^^^^^^^\n  File "{futures._base.__file__}", line 449, in result\n    return self.__get_result()\n           ^^^^^^^^^^^^^^^^^^^\n  File "{futures._base.__file__}", line 401, in __get_result\n    raise self._exception\n  File "{futures.thread.__file__}", line 58, in run\n    result = self.fn(*self.args, **self.kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "{__file__}", line 25, in div\n    return v1 / v2\n           ~~~^~~~\nZeroDivisionError: division by zero\n'
        )

    def test_context_var(self):
        user.set('new_user')
        thread = threads.Thread(target=fake_func_context_var)
        thread.start()
        result = thread.join()
        self.assertEqual(result, 'new_user')


def fake_func():
    sleep(1)
    return DateTime.now()

def fake_func_error():
    raise KeyError('MyKey')


class ThreadPoolTestCase(TestCase):

    def test_results(self):
        pool = threads.ThreadPool()
        pool.add(target=div, args=(1, 2))
        pool.add(target=div, args=(1, 4))
        pool.wait()
        self.assertEqual(len(pool.results), 2)
        self.assertIn(0.25, pool.results)
        self.assertIn(0.5, pool.results)

    def test_concurrency(self):
        pool = threads.ThreadPool(2)
        pool.add(target=fake_func)
        pool.add(target=fake_func)
        pool.wait()
        # The second call could finish before, so we need to get the min and max to check the delta
        min_value = min(pool.results)
        max_value = max(pool.results)
        # They run in the same second so the delta will be between 0 and 1
        delta = max_value - min_value
        self.assertLess(delta.total_seconds(), 1)
        self.assertGreater(delta.total_seconds(), 0)

    def test_concurrency_with_one_thread(self):
        pool = threads.ThreadPool(1)
        pool.add(target=fake_func)
        pool.add(target=fake_func)
        pool.wait()
        delta = pool.results[1] - pool.results[0]
        # The second run need to wait 1 second so the delta will be between 1 and 2
        self.assertLess(delta.total_seconds(), 2)
        self.assertGreater(delta.total_seconds(), 1)

    @mock.patch.object(threads.log, 'error')
    def test_silent_thread(self, error: mock.MagicMock):
        pool = threads.ThreadPool(concurrency=1, silent=True)
        pool.add(target=fake_func_error)
        pool.wait()
        error.assert_called_once_with(
            'Thread execution error -> target: %s, args: %s, kwargs: %s, traceback: %s',
            fake_func_error,
            (),
            {},
            f'Traceback (most recent call last):\n  File "{threads.__file__}", line 180, in wait\n    self.results.append(future.result())\n                        ^^^^^^^^^^^^^^^\n  File "{futures._base.__file__}", line 449, in result\n    return self.__get_result()\n           ^^^^^^^^^^^^^^^^^^^\n  File "{futures._base.__file__}", line 401, in __get_result\n    raise self._exception\n  File "{futures.thread.__file__}", line 58, in run\n    result = self.fn(*self.args, **self.kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File "{__file__}", line 66, in fake_func_error\n    raise KeyError(\'MyKey\')\nKeyError: \'MyKey\'\n'
        )

    @mock.patch.object(threads.log, 'error')
    def test_raise_thread(self, error: mock.MagicMock):
        pool = threads.ThreadPool(concurrency=1, silent=False)
        pool.add(target=fake_func_error)
        with self.assertRaisesRegex(KeyError, 'MyKey'):
            pool.wait()
        error.assert_not_called()

    def test_context_var(self):
        user.set('new_user')
        pool = threads.ThreadPool(concurrency=1)
        pool.add(target=fake_func_context_var)
        pool.wait()
        self.assertListEqual(pool.results, ['new_user'])
