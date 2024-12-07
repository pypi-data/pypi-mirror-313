""" Pretty user-logging """

import os
import textwrap
import tabulate
import inspect
import datetime as dt
import pytz
import logging
import pandas as pd
from pytensils import errors
from typing import Union, Callable

# Static variable(s)
INDENT = 4
LINE_LENGTH = 79
TIMEZONE = 'America/New_York'

# Private static variable(s)
_MAX_DEPTH = 1

# Setup CPython logging
pytensils = logging.getLogger('pytensils')
pytensils.setLevel(level=logging.DEBUG)

# Prevent propagation to the root logger to avoid duplicate messages
pytensils.propagate = False

# Setup a CPython logging stream handler
debugger = logging.StreamHandler()
debugger.setLevel(level=logging.DEBUG)
debugger.setFormatter(fmt=logging.Formatter('[DEBUG] %(message)s'))

# Add the handler if it does not currently exist
if not any(isinstance(h, logging.StreamHandler) for h in pytensils.handlers):
    pytensils.addHandler(hdlr=debugger)

# Setup tabulate
tabulate.PRESERVE_WHITESPACE = True


class Handler():
    """ A `class` that represents a logging-handler.

    Parameters
    ----------
    path : `str`
        Directory path to the folder that contains the `file_name` of the
            log-file.
    file_name : `str`
        File name of the log-file.
    description : `str`
        Information about the executed Python job run.
    metadata : `dict`
        Environment parameters to display as metadata about the executed
            Python job run.
    create: `bool`
        `True` or `False`, creates an empty log-file, `file_name`
            within `path` when `True`.
    debug_console: `bool`
        `True` or `False`, outputs the logging content to the console
            output when `True` using `logging.debug()`.
    """

    def __init__(
        self,
        path: str,
        file_name: str = 'python.log',
        description: str = 'Environment information summary.',
        metadata: dict = {},
        create: bool = True,
        debug_console: bool = False
    ):
        """ Initializes an instance of the logging-handler class.

        Parameters
        ----------
        path : `str`
            Directory path to the folder that contains the `file_name` of the
                log-file.
        file_name : `str`
            File name of the log-file.
        description : `str`
            Information about the executed Python job run.
        metadata : `dict`
            Environment parameters to display as metadata about the executed
                Python job run.
        create: `bool`
            `True` or `False`, creates an empty log-file, `file_name`
                within `path` when `True`.
        debug_console: `bool`
            `True` or `False`, outputs the logging content to the console
                output when `True` using `logging.debug()`.
        """

        # Assign class variables
        self.path = path
        self.file_name = file_name
        self.debug_console = debug_console

        # Assign private class variables
        self._INDENT = INDENT
        self._LINE_LENGTH = LINE_LENGTH
        self._TIMEZONE = TIMEZONE
        self._START_TIME = dt.datetime.now(tz=pytz.timezone(TIMEZONE))

        # Validate the file-path
        if not os.path.isdir(path):
            raise OSError('{%s} does not exist.' % (path))

        # Create the file-name
        if create:
            if os.path.isfile(
                os.path.join(path, file_name)
            ):
                # Remove the log-file if it exists
                os.remove(os.path.join(path, file_name))

            # Re-create the log-file
            with open(os.path.join(path, file_name), 'w'):
                pass

            # Initialize the content of the log-file
            self.write_header(
                header='Run information',
                divider=False
            )

            # Write metadata
            if metadata:
                tuples = [(k, v) for k, v in metadata.items()]
                tuples.insert(
                    0,
                    (
                        'Start time',
                        self._START_TIME.strftime('%Y-%m-%d %H:%M:%S')
                    )
                )
                metadata = dict(tuples)
            else:
                metadata = {
                    'Start time': (
                        self._START_TIME.strftime('%Y-%m-%d %H:%M:%S')
                    )
                }

            # Write job-information
            self.write(
                content=description
            )

            # Write parameters
            self.write(
                content=metadata
            )

        # Validate the file-name
        else:
            if not os.path.isfile(
                os.path.join(path, file_name)
            ):
                raise FileNotFoundError(
                    '{%s} does not exist within {%s}.' % (
                        file_name,
                        path
                    )
                )

    def write_header(
        self,
        header: str,
        divider: bool = True
    ):
        """ Writes `header` to the log-file.

        Parameters
        ----------
        header : `str`
            String to output as a header
        divider : `bool`
            `True` or `False`, writes a divider when `True`.
        """

        # Write
        with open(os.path.join(self.path, self.file_name), 'a+') as log:

            if isinstance(header, str):

                # Validate header
                if not len(header) > (self._LINE_LENGTH-self._INDENT):
                    log.write(
                        self._pretty_header(
                            header=header,
                            divider=divider
                        )
                    )
                else:
                    raise ValueError(
                        ''.join([
                            'The header value exceeds the',
                            ' maximum line length {%s}.' % (
                                self._LINE_LENGTH-self._INDENT
                            )
                        ])
                    )

            else:
                raise TypeError(
                    'Invalid header datatype {%s}.' % (
                        type(header).__name__
                    )
                )

    def write(
        self,
        content: Union[str, list, dict, pd.DataFrame],
        level: str = 'NOTSET'
    ):
        """ Writes `content` to the log-file with the `level` scope.

        Parameters
        ----------
        content : [`str`, `list`, `dict`, `pd.DataFrame`]
            The object to be written to the log-file.
        level : `str`
            Any level available by `logging`.

                e.g., [
                    'CRITICAL',
                    'ERROR',
                    'WARNING',
                    'INFO',
                    'DEBUG',
                    'NOTSET'
                ]
        """

        # Validate level
        _validate_level(level=level)

        # Retrive level substring
        substring = _return_level_substring(level=level)

        # Write
        with open(os.path.join(self.path, self.file_name), 'a+') as log:

            # `str`
            if isinstance(content, str):
                log.write(
                    self._pretty_str(
                        string=''.join([
                            substring,
                            content
                        ]),
                        level=level,
                        wrap=True
                    )
                )

            # `list`
            elif isinstance(content, list):
                log.write(
                    self._pretty_list(
                        list_object=content
                    )
                )

            # `dict`
            elif isinstance(content, dict):
                log.write(
                    self._pretty_dict(
                        dict_object=content
                    )
                )

            # `pd.DataFrame`
            elif isinstance(content, pd.DataFrame):
                log.write(
                    self._pretty_df(
                        df=content
                    )
                )

            else:
                raise TypeError(
                    'Invalid content datatype {%s}.' % (
                        type(content).__name__
                    )
                )

    def close(
        self
    ):
        """ Closes the log, writing run-time information about the job.
        """

        # Write header
        self.write_header(
            header='Run time',
            divider=True
        )

        # Write context
        self.write(
            content='Run-time performance summary.'
        )

        # Write run-time parameters
        end_time = dt.datetime.now(tz=pytz.timezone(TIMEZONE))
        self.write(
            content={
                'Start time': self._START_TIME.strftime('%H:%M:%S.%f'),
                'End time': end_time.strftime('%H:%M:%S.%f'),
                'Run time': str(end_time-self._START_TIME).zfill(15),
            }
        )

        # Write final divider
        self.write(content='')
        self.write(
            content=''.join(['-'*(self._LINE_LENGTH-self._INDENT-1), '\n'])
        )

    def close_on_exception(
        self,
        func: Callable
    ) -> Callable:
        """ Logs any unhandled exception raised by the `func` passed.

        Parameters
        ----------
        func : `Callable`
            Function object.
        """

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

            # Raise all `pytensils` exceptions
            except errors.config.all() as e:
                errors.config.raise_exception(
                    msg=(
                        'See {%s} for more information.' % (
                            os.path.join(
                                self.path,
                                self.file_name
                            )
                        )
                    ),
                    exception=e
                )

            # Raise all other exceptions
            except Exception as e:

                self.write_header(
                    header='Unhandled exception'
                )
                self.write(
                    content=(
                        'The process failed due to an unhandled exception.'
                    ),
                    level='CRITICAL'
                )
                self.write(content='')
                self.write(
                    content=''.join([
                        '>'*(self._INDENT-1),
                        ' ',
                        type(e).__name__,
                        ': ',
                        str(e)
                    ])
                )
                self.write(
                    content={
                        'Filename': inspect.trace()[-1][1],
                        'Line Number': 'Line %s' % inspect.trace()[-1][2],
                        'Function': '%s()' % inspect.trace()[-1][3],
                        'Exception': type(e).__name__
                    }
                )
                self.close()
                raise e
            return result
        return wrapper

    def _pretty_header(
        self,
        header: str,
        divider: bool = True
    ) -> str:
        """ Returns a 'pretty' formatted header.

        Parameters
        ----------
        header : `str`
            String to `pretty` format.
        divider : `bool`
            `True` or `False`, writes a divider when `True`.
        """

        # Prettify header
        if divider:
            return ''.join(
                [
                    self._pretty_str(
                        string=''
                    ),
                    self._pretty_str(
                        string='-'*(self._LINE_LENGTH-self._INDENT-1)
                    ),
                    self._pretty_str(
                        string=''
                    ),
                    self._pretty_str(
                        string=header
                    ),
                    self._pretty_str(
                        string='-'*len(header)
                    ),
                    self._pretty_str(
                        string=''
                    )
                ]
            )
        else:
            return ''.join(
                [
                    self._pretty_str(
                        string=header
                    ),
                    self._pretty_str(
                        string='-'*len(header)
                    ),
                    self._pretty_str(
                        string=''
                    )
                ]
            )

    def _pretty_str(
        self,
        string: str,
        level: str = 'NOTSET',
        wrap: bool = False
    ) -> str:
        """ Returns a 'pretty' formatted string.

        Parameters
        ----------
        string : `str`
            String to `pretty` format.
        level : `str`
            Any level available by `logging`.

                e.g., [
                    'CRITICAL',
                    'ERROR',
                    'WARNING',
                    'INFO',
                    'DEBUG',
                    'NOTSET'
                ]
        wrap : `bool`
            `True` or `False`, wraps the string based on `logging.LINE_LENGTH`
                when `True`.
        """

        # Cleanse string
        string = string.replace('\n', '').replace('\r', '')

        # Wrap string
        if wrap:
            strings = textwrap.wrap(
                text=string,
                width=self._LINE_LENGTH-self._INDENT-1,
                subsequent_indent=' '*self._INDENT
            )
        else:
            strings = [string]

        # Prettify string
        if level in ['CRITICAL', 'ERROR', 'WARNING']:
            string = '\n'.join(
                [
                    ''.join(
                        ['*'*(self._INDENT-1), ' ', string]
                    ) for string in strings[0:1]
                ]
                + [
                    ''.join(
                        [' '*self._INDENT, string]
                    ) for string in strings[1:]
                ]
            )
        else:
            string = '\n'.join(
                [''.join(
                    [' '*self._INDENT, string]
                ) for string in strings]
            )

        # Debug
        if self.debug_console:
            pytensils.debug(string.replace('\n', '\n[DEBUG] '))

        return ''.join([string, '\n'])

    def _pretty_list(
        self,
        list_object: list
    ) -> str:
        """ Returns a 'pretty' formatted list.

        Parameters
        ----------
        list_object : `list`
            List to `pretty` format.
        """

        # Prettify list
        return ''.join(
            [
                self._pretty_str(
                    string=''
                )
            ]
            + [
                self._pretty_str(
                    string=''.join([
                        ' '*self._INDENT,
                        '- ',
                        self._pretty_textwrap(
                            string=str(item),
                            width=(
                                self._LINE_LENGTH
                                - self._INDENT
                                - self._INDENT
                                - 3
                            )
                        )
                    ])
                ) for item in list_object
            ]
        )

    def _pretty_dict(
        self,
        dict_object: dict
    ) -> str:
        """ Returns a 'pretty' formatted dict.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary to `pretty` format.
        """

        # Prettify dictionary
        if self._validate_depth(dict_object=dict_object):

            # Retain the maximum key length
            max_key_length = max([len(i) for i in list(dict_object.keys())])

            return ''.join(
                [
                    self._pretty_str(
                        string=''
                    )
                ]
                + [
                    self._pretty_str(
                        string=''.join([
                            ' '*self._INDENT,
                            key,
                            ' '*(max_key_length-len(key)+self._INDENT),
                            ': ',
                            self._pretty_textwrap(
                                string=str(dict_object[key]),
                                width=(
                                    self._LINE_LENGTH
                                    - self._INDENT
                                    - self._INDENT
                                    - max_key_length
                                    - self._INDENT
                                    - 3
                                )
                            )
                        ])
                    ) for key in list(dict_object.keys())
                ]
            )
        else:
            raise ValueError(
                'The dictionary object depth exceeds the maximum depth of 1.'
            )

    def _pretty_df(
        self,
        df: pd.DataFrame
    ) -> str:
        """ Writes a 'pretty' formatted dataframe.

        Parameters
        ----------
        df : `pd.DataFrame`
            Dataframe to 'pretty' format.
        """

        # Prettify dataframe
        return ''.join(
            [
                self._pretty_str(
                    string=''
                )
            ]
            + [
                self._pretty_str(
                    string=''.join([
                        ' '*self._INDENT,
                        line
                    ])
                ) for line in tabulate.tabulate(
                    df,
                    headers='keys',
                    tablefmt='simple',
                    showindex=False,
                    floatfmt=',.2f',
                    intfmt=','
                ).split('\n')
            ]
        )

    def _validate_depth(
        self,
        dict_object: dict
    ) -> bool:
        """ Validates the depth of `dict_object`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object to validate.
        """
        if _return_dictionary_depth(
            dict_object=dict_object
        ) == _MAX_DEPTH:
            return True
        else:
            return False

    def _pretty_textwrap(
        self,
        string: str,
        width: int
    ) -> str:
        """ Returns a 'pretty' formatted shortened string.

        Parameters
        ----------
        string : `str`
            String to 'pretty' format.
        width : `int`
            The maximum width of the returned string.
        """
        if len(string) >= width and ' ' not in string:
            return '[...]'.join(
                [
                    string[:(width-round(width/2)-5)],
                    string[(len(string)-round(width/2)):]]
            )
        else:
            return textwrap.shorten(
                str(string),
                width=width,
                break_long_words=True
            )


def _validate_level(level: str):
    """ Validates the `level` scope for logging.

    Parameters
    ----------
    level : `str`
        Any level available by `logging`.

            e.g., [
                'CRITICAL',
                'ERROR',
                'WARNING',
                'INFO',
                'DEBUG',
                'NOTSET'
            ]
    """
    try:
        logging._checkLevel(level=level)
    except ValueError:
        raise ValueError(
            'Invalid level {%s}.' % (level)
        )


def _return_level_substring(level: str):
    """ Returns the substring corresponding to level.

    Parameters
    ----------
    level : `str`
        Any level available by `logging`.

            e.g., [
                'CRITICAL',
                'ERROR',
                'WARNING',
                'INFO',
                'DEBUG',
                'NOTSET'
            ]
    """
    if level == 'NOTSET':
        return ''
    else:
        return '%s: ' % (level)


def _return_dictionary_depth(
    dict_object: dict
) -> int:
    """ Returns the depth of a dictionary-object as an `int`.

    Parameters
    ----------
    dict_object : `dict`
        Dictionary object to parse.
    """
    counter = 0
    for i in str(dict_object):
        if i == "{":
            counter += 1
    return counter
