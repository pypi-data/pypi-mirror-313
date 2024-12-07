
# Everysk Lib

Welcome to the documentation for the Everysk Library!

Everysk's library was developed with the aim of unifying python
codes to be used in various company projects.

## API Reference

The [Everysk API](https://everysk.com/api/docs) is build around the standard [REST](https://en.wikipedia.org/wiki/REST) protocol and contains multiple endpoints to perform calculations, create portfolios, create workspaces where you can manage datastores, reports, files, workflows, and much more.

## Docker

Docker is used to create, run, and manage containers. In this project, Docker is used to set up a **PyPi** server and built the **Everysk library**.

### Running the PyPI Server.

To run the pypi server, first you will need to build a Docker image and then run a container from that image.

#### 1. Build the Docker image

The command below builds a Docker image using the Dockerfile located in the `./docker/` directory. The `--target` option specifies the build stage, which in this case is `everysk_pypi_server`. The `--tag` option assigns a name and tag to the image, `everysk_pypi_server:latest`.

```bash
  docker build --file ./docker/Dockerfile --target everysk_pypi_server --tag everysk_pypi_server:latest .
```

#### 2. Run the Docker container

After that, you will need to run the Docker container from the image built in the previous step. The `--rm` option removes the container when it exits. The `-it` option allows you to interact with the container. The `-e` option sets the environment variable `PYPI_PASSWORD` to '123123'. The `-p` options map the host ports 8080 and 2020 to the container ports 80 and 22 respectively.

```
  docker run --rm -it -e PYPI_PASSWORD='123123' -p 0.0.0.0:8080:80 -p 0.0.0.0:2020:22 everysk_pypi_server:latest
```

### Building the library and Sending to PyPI Server

To build the library and send to Pypi server, you will need to build another Docker image and run, once again, a container from that image.

#### 1. Build the Docker Image

We use a command that is similar to the one used to build the PyPI server image, the only thing that differs is the target build stage and tag.

```bash
  docker build --file ./docker/Dockerfile --target everysk_lib_build --tag everysk_lib_build:latest .
```

#### 2. Run the Docker container

After building the docker image, we run a Docker container from the image built in the previous step. The environment variables `PYPI_PASSWORD` and `PYPI_HOST` are set to '123123' and '192.168.0.116' respectively.

```
  docker run --rm -it -e PYPI_PASSWORD='123123' -e PYPI_HOST='192.168.0.116' everysk_lib_build:latest
```

## Usage/Examples

Let's have a look at the different modules available from the everysk library

### Compress Module

The **compress** module from `everysk.core` allows the compression and decompression of JSON files and Python objects. It includes functions to serialize objects into JSON strings or pickle objects, then it compresses or decompresses them using the zlib or gzip module.

Below we have an implementation example of one of the methods inside the module.

```python
    >>> from everysk.core.compress import compress
    >>> data = {'key' : 'value'}
    >>> compressed_data = compress(data)
    b'x\x9c\xcbH\xcd\xc9\xc9W(....) # example of the compressed data
```

### Exceptions Module

This module is a collection of custom exception classes designed to handle errors then raise specific exceptions based on those errors. They also provide attributes and methods to improve the debugging experience.

Below we have an example of the `DateError` exception being raised after we passed an invalid input to a hypothetical function.

```python
    >>> from everysk.core.exceptions import DateError
    >>> try:
    ...     result = validate_month_day('2024-01-01')
    ...     return result
    >>> except:
  ...       raise DateError('invalid date format')
```

### Object & Fields Module

The **object** and **fields** modules from the `everysk.core` package are used to create classes with consistent and type-checked data.

Here's an example of how to use them:

```python
    >>> from everysk.core.fields import BoolField
    >>> from everysk.core.object import BaseDict
    >>>
    >>> class MyClass(BaseDict):
    ...     field: BoolField(required=True)
    >>>
    >>> obj = MyClass(field=True)
    >>> obj.field is True
    ... True
    >>> obj.field == obj['field']
    ... True
```

### HTTP Module

Module **http.py** module provides a set of classes for handling HTTP requests within the `everysk` framework, it is designed to facilitate HTTP communications, including specific error checking and functionalities for dealing with authentication.

```python
    >>> from everysk.core.http import HttpGETConnection
    >>>
    >>> class MyConnection(HttpGETConnection):
    ...     url: StrField(default='https://example.com', readonly=True)
    ...     def get_params(self) -> dict:
    ...         # Will be added to url p=1&p=2
    ...         return {'p': 1, 'p': 2}
    ...
    ...     def message_error_check(self, message: str, status_code: int) -> bool:
    ...         # If this message appear on HttpError then we try again.
    ...         return 'server is busy' in message
    >>>
    >>> response = MyConnection().get_response()
```

### Settings Module

Module **settings** is the sum of all settings.py created on the project.
Every setting will have it's value first from env otherwise from the attribute.

```python
    >>> from everysk.config import settings
    >>> settings.DEBUG
    True
```

### Log Module

The **log** module from `log.py` includes a collection of methods and classes designed to handle logging operations.

```python
    >>> from everysk.core.log import Logger
    >>> log = Logger(name='log-test')
    >>> log.debug('Test')
    '2024-02-07 12:49:10,640 - DEBUG - {} - Test'
```

The log module also has useful methods like the `slack()` method from the `Logger` class which can send slack messages to a channel using the **Slack WebHooks**. Check out their [documentation](https://api.slack.com/messaging/webhooks).

Let's have a look at how the `slack()` method is used:

```python
    >>> from everysk.core.log import Logger
    >>> slack_instantiation = Logger()
    >>> slack_instantiation.slack(title='title of the message', message='body of the message', color='danger')
    '2024-05-23 13:17:22,734 - Slack message: title of the message -> body of the message'
```

### Workers Module

The `workers.py` file provides a framework for managing and executing tasks using Google Cloud Tasks within the `everysk` ecosystem. It utilizes Google Cloud Tasks to enqueue and process asynchronous tasks, suitable for handling operations that require delay or scheduling.

Below we have an usage example of deploying tasks using the `TaskGoogle` class:

```python
    >>> from everysk.core.workers import TaskGoogle
    >>> task = TaskGoogle(worker_url='https://example.com/worker', worker_id='example_worker_id')
    >>> task.save(timeout=30.0, retry_times=3)
```

This example shows how to initialize a task with a specific worker URL and worker ID, then save it to [**Google Cloud Tasks**](https://cloud.google.com/tasks/docs).

### Firestore Module

Module **firestore.DocumentCached** is a Redis/Firestore document. This uses Redis for
read the data and Redis/Firestore to store the data. To keep the cache synchronized
with Firestore, use everysk/cloud_function. With this when we alter the data using
Firestore interface the cache will be updated.

```python
    >>> from everysk.core.firestore import DocumentCached
    >>> doc = Document(_collection_name='collection', firestore_id='firestore_id')
    >>> doc.firestore_id
    'firestore_id'
```

### String Module

The `string.py` module in the `everysk` library provides a handful of utility functions designed for string manipulation and validation, this is useful for handling text data in a variety of programming and data processing contexts.

Below we have an example of the `pluralize()` method that transforms the string into it's pluralized version

```python
    >>> from everysk.core.string import pluralize
    >>> pluralize('system')
    'systems'
```

Below is another example of a method that converts the current string into the snake case format.

```python
    >>> from everysk.core.string import snake_case
    >>> snake_case('CustomIndex')
    'custom_index'
```

### Threads Module

The `threads.py` module offers different methods for managing [concurrent execution](https://en.wikipedia.org/wiki/Concurrent_computing) using threads, tailored specifically for environments that require parallel processing.

Below we have an example of code that executes a task asynchronously with a simple thread management.

```python
    >>> from everysk.core.threads import Thread

    >>> def sum(a: int, b: int) -> int:
    ...     return a + b
    ...
    >>> thread = Thread(target=sum, args=(1, 2))
    >>> task.start()
    >>> task.join()
    3
```

This module is proved to be useful for applications within the `everysk` infrastructure that require parallel computation or asynchronous task management.

### Serialize Module

The serialize module is designed to handle serialization and deserialization of complex Python objects to and from JSON format, with specific support for dates, custom objects, and structured data.

Here is an example for serializing a Python object to a JSON string in bytes:

```python
    >>> from everysk.core.serialize import dumps
    >>> class MyClass:
    ...     def __init__(self, worker_name, worker_id):
    ...         self.worker_name = worker_name
    ...         self.worker_id = worker_id
    ...
    >>> def _default(obj):
    ...     if isinstance(obj, MyClass):
    ...         return obj.__dict__
    ...     raise TypeError(f'Type {type(obj)} is not serializable')
    ...
    >>> my_obj = MyClass('sample_worker', 'sample_worker_id')
    >>> serialized_data = dumps(my_obj, default=_default)
```

### Number Module

The `number.py` module is designed to provide utility functions related to numerical operations.

Below we have an implementation of the function `is_float_convertible` that returns a boolean indicating whether the value can be converted to a float point value or not.
```python
    >>> from everysk.core.numbers import is_float_convertible
    >>> is_float_convertible('3.14')
    True

    >>> is_float_convertible(5)
    True

    >>> is_float_convertible('not a float')
    False
```

### Redis Module

The **Redis** module is designed to interact with a Redis server to store, retrieve and manage cached data.

Below is an example of how to use the `acquire()` method to verify if a key is locked by the current lock.

```python
    >>> from everysk.core.redis import RedisLock
    >>> redis_lock = RedisLock(name='test_name', timeout=1, host='1.0.0.0', port=4435)
    >>> redis_lock.acquire('example_lock_key')
    'Lock acquired for key "example lock_key"'
```

## Installation

Here you can access the instructions on how to install the `everysk-beta` library using pip.

To install the `everysk-beta` library, you will need to use pip's `install` command along with the `--index-url` option that allows you to specify the PyPI server from which to install the package.

Replace `PYPI_HOST` with the actual host of your PyPI server. Then run the following command:

```bash
  pip install --index-url https://PYPI_HOST everysk-beta
```

### Verifying the Installation

After installing the library, it's a good practice to verify if the installation was successful. Here is how to achieve this:

#### 1. Open a terminal

#### 2. Start the Python interpreter by typing `python` and pressing `Enter`

#### 3. In the Python interpreter, type the following command then press `Enter`:

```python
  import everysk
```

If the library has been installed correctly, this command should complete without any errors. If the library is not installed or there's a problem with the installation, Python will raise a `ModuleNotFoundError`


## Running Tests

This section provides instructions on how to run tests for the project. There are two scenarios, the first one is running tests in a development environment and the second one is running tests after the library has been installed from PyPI.

### Running Tests in Development Environment

In a development environment you can use the provided shell script to run the tests. The script sets up the necessary environment and then run the tests. To execute the tests, open a bash terminal and run the following command.

```bash
  ./run.sh tests
```

### Running Tests After the Library is Installed

After the library has been installed in your project from PyPI, you can start running tests using Python's built-in unittest module. To run tests use the following command:


```bash
  python3 -m unittest everysk.core.tests
```

The command uses Python's unittest module as mentioned above as a script, which then runs the test in the `everysk.core.tests` package.


## Running Tests with coverage

Code coverage us a way of measuring how many lines of code are executed while the automated tests are running.

To run tests along with a coverage report, you can use the provided shell script. The script will not only run the tests but also generate a coverage report that shows the percentage of code that was executed during the tests.

This is useful to identify sections of your code that are not being tested and may need additional tests.

#### 1. Open a terminal in your Visual Studio Code environment.

#### 2. Run the following command.

```bash
  ./run.sh coverage
```

This command executes the `run.sh` script with the `coverage` argument. The report will be displayed in the terminal after the script completed the tests.

**Remember:** a high coverage percentage is generally good, but 100% coverage does not ensures that your code is free from bugs or any other problem that might occur in your code. The full coverage just means that all the lines in your code were executed during the tests.


## Contributing

Contributions are always welcome and greatly appreciated!

Go to the repository [link](https://github.com/Everysk/everysk-lib) and click on the `Fork` button to create your own copy of the everysk library.

Then clone the project in your own local machine by running the command below or using the **GitHub Desktop**.

```bash
  git clone https://github.com/<your-username>/everysk-lib.git everysk-yourusername
```

This section creates a directory called `everysk-yourusername` to center all your code.

After that you can change the directory by:

```bash
  cd everysk-yourusername
```

Create the **upstream** repository which will refer to the main repository that you just forked.

```bash
  git remote add upstream https://github.com/Everysk/everysk-lib.git
```

Now run the following commands to make sure that your clone is up-to-date with main everysk repository

```bash
  git checkout main
  git pull upstream main
```

Shortly after, create a new branch to add your code

```bash
  git checkout -b brand-new-feature
```

The command above will automatically switch to this newly created branch. At this moment your are able to make your modifications to the code and commit locally as you progress.

After all the code changes, you can submit your contribution by pushing the changes to your fork on GitHub:

```bash
  git push origin brand-new-feature
```

The command above ensures that all the modifications that you've made are up-to-date with your current branch.

At the end of this process you will need to make a **Pull Request** to the main branch.

To achieve this, go to the GitHub page of the project and click on the `Pull requests` tab, then click on `New pull request` button.

This will open a new section used to compare branches, now choose your branch for merging into the main branch and hit the `Create pull request` button.

## License

(C) Copyright 2023 EVERYSK TECHNOLOGIES

This is an unpublished work containing confidential and proprietary
information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
without authorization of EVERYSK TECHNOLOGIES is prohibited.

Date: Jan 2023

Contact: contact@everysk.com

URL: https://everysk.com/
