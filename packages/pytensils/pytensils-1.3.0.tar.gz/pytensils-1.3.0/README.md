# pytensils

|         |                                                                                                      |
| ------- | ---------------------------------------------------------------------------------------------------- |
| Tests   | [![Unit-Tests](https://github.com/thomaseleff/pytensils/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/thomaseleff/pytensils/actions/workflows/unit-tests.yml) [![Coverage](https://raw.githubusercontent.com/thomaseleff/pytensils/main/coverage/coverage.svg)](https://github.com/thomaseleff/pytensils/blob/main/coverage/COVERAGE.md) |
| Package | [![PyPI latest release](https://img.shields.io/pypi/v/pytensils.svg)](https://pypi.org/project/pytensils/) [![PyPI downloads](https://img.shields.io/pypi/dm/pytensils.svg?label=PyPI%20downloads)](https://pypi.org/project/pytensils/) [![License - MIT](https://img.shields.io/pypi/l/pytensils.svg)](https://github.com/thomaseleff/pytensils/blob/main/LICENSE) [![Supported versions](https://img.shields.io/pypi/pyversions/pytensils.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/pytensils/) |

`pytensils` is a Python package that provides general utility functions for managing configuration, user-logging, directories and data-types as well as a basic run-time profiler.

# Installation
The source code is available on [GitHub](https://github.com/thomaseleff/pytensils).

```
# Via PyPI
pip install pytensils
```

# Documentation & examples
An overview of all public `pytensils` objects, functions and methods exposed within the `pytensils.*` namespace.

- `.config` [Configuration-file management](#configuration-file-management)
- `.logging` [User-logging](#user-logging)
- `.utils` [General utilities](#general-utilities)
- `.profiler` [Run-time profiler](#run-time-profiler)

## Configuration-file management
`.config` contains the `class` methods for reading, writing and validating `.json` format configuration-files. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/config.py) code via GitHub.

### Initialize an instance of the config-handler
The `config.Handler(path: str, file_name: str, create: bool = False, Logging: pytensils.logging.Handler | None = None)` constructor initializes an instance of the config `class` and validates that `path` and `file_name` exist. Should the `path` not exist, the constructor raises an `OSError`. Should the `file_name` not exist, the constructor raises a `FileNotFoundError`. Should the content not be able to be parsed as `json`, the constructor raises a `TypeError`.

 **Advanced parameters**

- The parameter `create` can be set to `False` to initialize an instance of the `class` without reading config-data from `/path/file_name`. The `create` parameter is useful in order to generate the configuration-file via the Python process.
- The parameter `Logging` can be set to an instance of the `pytensils.logging.Handler` `class` to enable pretty user-logging for config-related read, write and validation errors natively.

``` python
import os
from pytensils import config

"""
    Assume there is a file, named './config.json' within the same folder
    as the executed Python process with the following contents,

        {
            "config": {
                "str": "ABC",
                "bool": true,
                "int": 1,
                "float": 9.9,
                "list": ["A", "B", "C"]
            }
        }

"""

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)
```

### Access or re-load the configuration-file data
The configuration-file data can be accessed via a `class` variable, `.data`, returned as a copy as a dictionary, `.to_dict()`, or read directly from the source `.json` file, `.read()`.

``` python
import os
from pytensils import config

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)

# Access the configuration-file data directly via a `class` variable
print(Config.data)

# Return a copy of the configuation-file data as a dictionary
config_dictionary = Config.to_dict()
print(config_dictionary)

# Re-load the configuration-file data
print(Config.read())
```

### Validate the configuration-file
The `.validate(dtypes: dict)` function validates that the structure of `config` matches the structure of `dtype` and returns `True` when validation is successful. The function raises any type errors within the console output as a `config.ValidationError` when validation fails.

``` python
import os
from pytensils import config

# Dictionary of expected data-types
dtype_dict_object = {
    "config": {
        "str": "str",
        "bool": "bool",
        "int": "int",
        "float": "float",
        "list": "list",
        "dict": "dict"
    }
}

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)

# Validate
if config.validate(dtypes=dtype_dict_object):
    print('NOTE: Validation succeeded.')
```

### Write a dictionary to a `.json` configuration-file
The `.write()` method writes the configuration-file data to a `.json` file while the `.from_dict(dict_object: dict, dtypes: dict | None = None)` method replaces the configuration-file data and writes the data to a `.json` file. When a dictionary is passed to `.from_dict` as `dtypes`, the function also validates `dict_object` based on the data-types in `dtypes`.

``` python
import os
from pytensils import config

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)

# Change the value of the "str" parameter within the "config" object
Config.data['config']['str'] = "DEF"

# Write
Config.write()

# Replace the configuration-file data and write, without validation
Config.from_dict(
    dict_object={
        "config": {
            "str": "DEF",
            "bool": True,
            "int": 1,
            "float": 9.9,
            "list": ["A", "B", "C"]
        }
    }
)
```

## User-logging
`.logging` contains the `class` methods for writing 'pretty' user-logging as well as a decorator for catching and logging unhandled exceptions raised during the execution of functions. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/logging.py) code via GitHub.

Access an example user-log, [example.log](https://github.com/thomaseleff/pytensils/blob/main/tests/resources/example.log), that show-cases `.logging` functionality via GitHub.

### Set-up logging
The `logging` library contains various static control variables that can be configured for all instances of the `logging.Handler` within a single Python session.

- `logging.INDENT`, the number of space-characters for the standard log-indentation (default = 4).
- `logging.LINE_LENGTH`, the maximum number of characters for a line of content (default = 79). For content longer than `logging.LINE_LENGTH`, `str` type content is automatically wrapped while `list` or `dict` type content is truncated. `logging.LINE_LENGTH` does not apply to `pd.DataFrame` type content.
- `logging.TIME_ZONE`, the time-zone for representing start and end time values (default = 'America/New_York'). Access the list of available [timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) via Wikipedia.

``` python
from pytensils import logging

# Set-up
logging.INDENT = 4
logging.LINE_LENGTH = 79
logging.TIME_ZONE = 'America/Chicago'
```

### Initialize an instance of the logging-handler
The `logging.Handler(path: str, file_name: str = 'python.log', description: str = 'Environment information summary.', metadata: dict, create: bool = True, debug_console: bool = False)` constructor initializes an instance of the logging `class` and validates that `path` exists. The constructor also validates that `file_name` exists when `create=False`. Should the `path` not exist, the constructor raises an `OSError`. Should the `file_name` not exist, the constructor raises a `FileNotFoundError`.

**Advanced parameters**

- The parameter `create` can be set to `False` to initialize an instance of the `class` without creating the `.log` file. The `create` parameter is useful so that multiple Python processes can write to the same user-log without overwriting the `.log` file.
- The parameter `debug_console` can be set to `True` to force outputting all content to the output console, in addition to the user-log.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)
```
```
User-log content
----------------

>    Run information
>    ---------------
>    
>    Environment information summary.
>    
>        Start time    : 2024-03-22 01:35:22
```

### Write a header to the user-log
The `.write_header(header: str, divider: bool)` method writes a pretty-styled header to the user-log. Should the header length exceed the `logging.LINE_LENGTH` parameter then the function raises a `ValueError`. Should the header not be of type `str` then the function raises a `TypeError`.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Write header
Logging.write_header(
    header='Task-information'
)

```
```
User-log content
----------------

>    --------------------------------------------------------------------------
>
>    Task-information
>    ----------------
```

### Write a status message to the user-log
The `.write(content: str | list | dict | pd.DataFrame, level: str)` method writes a pretty-styled content object to the user-log. The function supports content objects of type `str`, `list`, `dict` and `pd.DataFrame`. Should the content not be of any of the allowed types then the function raises a `TypeError`.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Write header
Logging.write_header(
    header='Examples: `str`'
)

# Write `str`
Logging.write(
    content='This is a critical error string',
    level='CRITICAL'
)
Logging.write(
    content=''.join([
        'This is an error string that exceeds the',
        ' line-length limit set for the log-file.'
    ]),
    level='ERROR'
)
Logging.write(
    content='This is a warning string.',
    level='WARNING'
)
Logging.write(
    content='This is a debug string.',
    level='DEBUG'
)
Logging.write(
    content=''.join([
        'This is a boring short story.'
        ' The quick brown fox jumped over the lazy dog.'
        ' The end.'
    ]),
    level='INFO'
)
Logging.write(
    content='This is an unset string.'
)
```
```
User-log content
----------------

>    --------------------------------------------------------------------------
>
>    Examples: `str`
>    ---------------
>    
>*** CRITICAL: This is a critical error string
>*** ERROR: This is an error string that exceeds the line-length limit set for
>        the log-file.
>*** WARNING: This is a warning string.
>    DEBUG: This is a debug string.
>    INFO: This is a boring short story. The quick brown fox jumped over the
>        lazy dog. The end.
>    This is an unset string.
```

### Write a list to the user-log
Cont'd examples related to the `.write(content: str | list | dict | pd.DataFrame, level: str)` method. 

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Write header
Logging.write_header(
    header='Examples: `list`'
)

# Write `list`
Logging.write(
    content='This is a list output.'
)
Logging.write(
    content=[
        ' '.join(str(i) for i in list(range(52))),
        ['A', 'B', 'C'],
        ('A', 'B', 'C'),
        1,
        2,
        3,
    ]
)
```
```
User-log content
----------------

>    --------------------------------------------------------------------------
>
>    Examples: `list`
>    ----------------
>   
>    This is a list output.
>    
>        - 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 [...]
>        - ['A', 'B', 'C']
>        - ('A', 'B', 'C')
>        - 1
>        - 2
>        - 3
```

### Write a dictionary to the user-log
Cont'd examples related to the `.write(content: str | list | dict | pd.DataFrame, level: str)` method. Currently, only dictionaries with a depth of 1 are supported. Should a dictionary with depth > 1 be passed, the function raises a `ValueError`.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Write header
Logging.write_header(
    header='Examples: `dict`'
)

# Write `dict`
Logging.write(
    content='This is a dictionary output.'
)
Logging.write(
    content={
        'A': 'a',
        'B': 'b',
        '123s': ' '.join(str(i) for i in list(range(52))),
        'Nineteen characters': 19,
        'List': ['A', 'B', 'C'],
        'Tupple': ('A', 'B', 'C')
    }
)
```
```
User-log content
----------------

>    --------------------------------------------------------------------------
>
>    Examples: `dict`
>    ----------------
>   
>    This is a dictionary output.
>    
>        A                      : a
>        B                      : b
>        123s                   : 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 [...]
>        Nineteen characters    : 19
>        List                   : ['A', 'B', 'C']
>        Tupple                 : ('A', 'B', 'C')
```

### Write a dataframe to the user-log
Cont'd examples related to the `.write(content: str | list | dict | pd.DataFrame, level: str)` method.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Write header
Logging.write_header(
    header='Examples: `pd.DataFrame`'
)

# Write `pd.DataFrame`
Logging.write(
    content='This is a dataframe output.'
)
Logging.write(
    content=pd.DataFrame(
        {
            "Calories": [420, 380, 390],
            "Duration": [50, 40, 45],
            "Day": ['Monday', 'Tuesday', 'Wednesday']
        }
    )
)
```
```
User-log content
----------------

>    --------------------------------------------------------------------------
>
>    Examples: `pd.DataFrame`
>    ------------------------
>   
>    This is a dataframe output.
>    
>          Calories    Duration  Day
>        ----------  ----------  ---------
>               420          50  Monday
>               380          40  Tuesday
>               390          45  Wednesday
```

### Close the user-log
The `.close()` method writes a pretty-styled run-time summary and closes the user-log.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Close
Logging.close()
```
```
User-log content
----------------

>    --------------------------------------------------------------------------
>
>    Run information
>    ---------------
>    
>    Environment information summary.
>    
>        Start time    : 2024-03-22 01:35:22
>    
>    --------------------------------------------------------------------------
>    
>    Run time
>    --------
>    
>    Run-time performance summary.
>    
>        Start time    : 01:35:22.098505
>        End time      : 01:35:22.183973
>        Run time      : 00:00:00.085468
>
>    --------------------------------------------------------------------------
```

### Close the user-log on unhandled exceptions
The `close_on_exception(func: Callable)` decorator function returns the result of `func` and closes the user-log reporting any unhandled exceptions as critical errors raised by `func` before raising the exception.

``` python
import os
from pytensils import logging

# Initialize the logging handler `class`
Logging = logging.Handler(
    path=os.path.dirname(__file__)
)

# Define function that fails with an unhandled-exception
@Logging.close_on_exception
def divide_by_zero():
    return 1 /0

if __name__ == "__main__":
    divide_by_zero()
```
```
User-log content
----------------

>    Run information
>    ---------------
>    
>    Environment information summary.
>    
>        Start time    : 2024-03-22 01:35:22
>    
>    --------------------------------------------------------------------------
>    
>    Unhandled exception
>    -------------------
>    
>*** CRITICAL: The process failed due to an unhandled exception.
>
>    >>> ZeroDivisionError: division by zero
>    
>        Filename       : ~\example.py
>        Line Number    : Line 12
>        Function       : divide_by_zero()
>        Exception      : ZeroDivisionError
>    
>    --------------------------------------------------------------------------
>    
>    Run time
>    --------
>    
>    Run-time performance summary.
>    
>        Start time    : 01:35:22.234821
>        End time      : 01:35:22.520567
>        Run time      : 00:00:00.285746
>
>    --------------------------------------------------------------------------
```

## General utilities
`.utils` contains the general functions for generating output directories and parsing data-types. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/utils.py) code via GitHub.

### Generate an output directory
The `generate_output_directory(path: str, root: str, sub_folders: list | None)` function generates an output directory within `path` that contains `root` and all `sub_folders`. Should `root` already exist in `path`, the function raises an `OSError`.

``` python
import os
from pytensils import utils

# Create an output directory, called 'Outputs' with two sub-folders, 'A' and 'B'
utils.generate_output_directory(
    path=os.path.dirname(__file__),
    root='Outputs',
    sub_folders=['A', 'B']
)
```

### Parse a string value into any data-type
The `as_type(value: str, return_dtype: str)` function parses a string `value` into the `return_dtype` and returns `value` as that type. Should `value` not convert into `return_dtype`, the function raises a `TypeError`. If the `return_dtype` is invalid, the function raises a `NameError`.

``` python
from pytensils import utils

# Parse a string value into an `int`
int_value = utils.as_type(
    value='1',
    return_dtype='int'
)

# Parse a list as a string into a `list`
list_object = utils.as_type(
    value='["A", "B", "C"]',
    return_dtype='list'
)
```

## Run-time profiler
`.profiler` contains the general run-time decorator for timing the execution of functions. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/profiler.py) code via GitHub.

### Time the execution of a function
The `run_time(func: Callable)` decorator function returns the result of `func` and prints the execution time of `func` within the console output.

``` python
import time
from pytensils import profiler

# Write and time a function that waits 1-second
@profiler.run_time
def wait_1_second():
    time.sleep(1)

if __name__ == "__main__":
    wait_1_second()
```
```
Output
------

> [INFO] Function {wait_1_second()} executed in 00:00:01 hh:mm:ss
```