"""
Information
---------------------------------------------------------------------
Name        : test_logging.py
Location    : ~/tests

Description
---------------------------------------------------------------------
Tests methods within `pytensils.logging`.
"""

import os
from io import StringIO
import pandas as pd
import logging as clogging
import pytest
from pytensils import logging, errors

PATH = os.path.join(
    os.path.dirname(__file__),
    'resources'
)


@pytest.fixture
def LOGGING_FIXTURE():
    return logging.Handler(
        path=PATH,
        file_name='example.log',
        description=''.join([
            'Generates example user-log content for',
            ' all `pytenstils.logging` functionality.'
        ]),
        metadata={
            'Extra parameter (1)': 1,
            'Extra parameter (2)': 2
        },
        create=True,
        debug_console=False
    )


def test_logging_success(LOGGING_FIXTURE: logging.Handler):

    string = ''.join([
        'This string is longer than 89 characters',
        ' and will be truncated causing an empty string to be displayed.'
    ])
    string_no_whitespace = string.replace(' ', '')

    # Generate `str` test(s)
    LOGGING_FIXTURE.write_header(
        header='Examples: `str`'
    )
    LOGGING_FIXTURE.write(
        content='This is a critical error string',
        level='CRITICAL'
    )
    LOGGING_FIXTURE.write(
        content=''.join([
            'This is an error string that exceeds the',
            ' line-length limit set for the log-file.'
        ]),
        level='ERROR'
    )
    LOGGING_FIXTURE.write(
        content='This is a warning string.',
        level='WARNING'
    )
    LOGGING_FIXTURE.write(
        content='This is a debug string.',
        level='DEBUG'
    )
    LOGGING_FIXTURE.write(
        content=''.join([
            'This is a boring short story.'
            ' The quick brown fox jumped over the lazy dog.'
            ' The end.'
        ]),
        level='INFO'
    )
    LOGGING_FIXTURE.write(
        content='This is an unset string.'
    )

    # Generate `list` test(s)
    LOGGING_FIXTURE.write_header(
        header='Examples: `list`',
        divider=True
    )
    LOGGING_FIXTURE.write(
        content='This is a list output.'
    )
    LOGGING_FIXTURE.write(
        content=[
            string,
            string_no_whitespace,
            ' '.join(str(i) for i in list(range(52))),
            ['A', 'B', 'C'],
            ('A', 'B', 'C'),
            1,
            2,
            3,
        ]
    )

    # Generate `dict` test(s)
    LOGGING_FIXTURE.write_header(
        header='Examples: `dict`',
        divider=True
    )
    LOGGING_FIXTURE.write(
        content='This is a dictionary output.'
    )
    LOGGING_FIXTURE.write(
        content={
            'A': 'a',
            'B': 'b',
            'With whitespace, > 89-chars': string,
            'No whitespace, > 89-chars': string_no_whitespace,
            '123s': ' '.join(str(i) for i in list(range(52))),
            'Nineteen characters': 19,
            'List': ['A', 'B', 'C'],
            'Tupple': ('A', 'B', 'C')
        }
    )

    # Generate `pd.DataFrame` test(s)
    LOGGING_FIXTURE.write_header(
        header='Examples: `pd.DataFrame`',
        divider=True
    )
    LOGGING_FIXTURE.write(
        content='This is a dataframe output.'
    )
    LOGGING_FIXTURE.write(
        content=pd.DataFrame(
            {
                "Calories": [420, 380, 390],
                "Duration": [50, 40, 45],
                "Day": ['Monday', 'Tuesday', 'Wednesday']
            }
        )
    )

    # Close
    LOGGING_FIXTURE.close()

    # Iterate and compare logs
    test = open(os.path.join(PATH, 'example.log'), 'r')
    compare = open(os.path.join(PATH, 'compare.log'), 'r')

    test_lines = test.readlines()
    compare_lines = compare.readlines()

    test.close()
    compare.close()

    # Assert both test and compare are the same length
    assert len(test_lines) == len(compare_lines)

    # Assert test and compare contain the same content
    #   Skip lines 6, 76, 77, 78 as these contain
    #   date-time values that cannot be compared due
    #   to different execution windows.
    for index in range(len(test_lines)):
        if index not in [6, 76, 77, 78]:
            assert test_lines[index] == compare_lines[index]


def test_init_oserror():
    with pytest.raises(OSError):
        _ = logging.Handler(
            path=os.path.join(
                os.path.dirname(__file__),
                'path-does-not-exist'
            ),
        )


def test_init_filenotfounderror():
    with pytest.raises(FileNotFoundError):
        _ = logging.Handler(
            path=PATH,
            file_name='file-not-found.log',
            create=False
        )


def test_write_header_valueerror():
    with pytest.raises(ValueError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        Logging.write_header(
            header='X'*(logging.LINE_LENGTH-logging.INDENT+1)
        )


def test_write_header_typeerror():
    with pytest.raises(TypeError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        Logging.write_header(
            header=1
        )


def test_write_typeerror():
    with pytest.raises(TypeError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        Logging.write(
            content=('A', 1)
        )


def test_debug_console():

    # Initialize logging
    Logging = logging.Handler(
        path=os.path.join(
            os.path.dirname(__file__),
            'resources'
        ),
        create=True,
        debug_console=True
    )

    # Ensure that a StreamHandler is attached
    handler = next(
        (
            h for h in logging.pytensils.handlers if isinstance(
                h,
                clogging.StreamHandler
            )
        ),
        None
    )
    assert handler is not None

    # Replace the StreamHandler with StringIO
    log_output = StringIO()
    original_stream = handler.stream
    handler.setStream(log_output)

    try:

        # Loging
        test_message = "Log-content-for-the-output-console"
        Logging.write(test_message)

        # Flush the handler and retrieve the log output
        handler.flush()
        log_output.seek(0)
        captured_logs = log_output.read()

        # Ensure the log message is present in the captured output
        assert test_message in captured_logs
        assert "DEBUG" in captured_logs

    finally:

        # Restore the StreamHandler
        handler.setStream(original_stream)

        # Cleanup
        os.remove(
            os.path.join(
                os.path.dirname(__file__),
                'resources',
                'python.log'
            )
        )


def test_pretty_dict_valueerror():
    with pytest.raises(ValueError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        # Cleanup
        os.remove(
            os.path.join(
                os.path.dirname(__file__),
                'resources',
                'python.log'
            )
        )

        _ = Logging._pretty_dict(dict_object={'A': {'B': {'C': 'c'}}})


def test_validate_level_valueerror():
    with pytest.raises(ValueError):
        logging._validate_level(level='unknown-logging-level')


def test_logging_close_on_exception_success():

    # Initialize logging
    Logging = logging.Handler(
        path=os.path.join(
            os.path.dirname(__file__),
            'resources'
        ),
        file_name='closes-on-exception-success.log',
        description=''.join([
            'Generates close-on-exception content for',
            ' `pytenstils.logging` functionality.'
        ]),
        create=True,
        debug_console=False
    )

    @Logging.close_on_exception
    def divide_by_1():
        return 1 / 1

    assert divide_by_1() == 1

    # Close
    Logging.close()


def test_logging_close_on_exception_zerodivisionerror():
    with pytest.raises(ZeroDivisionError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception.log',
            description=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def divide_by_zero():
            return 1 / 0

        divide_by_zero()


def test_logging_close_on_exception_oserror():
    with pytest.raises(OSError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception-oserror.log',
            description=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def raise_oserror():
            errors.config.raise_exception(
                msg='',
                exception=errors.config.OSError()
            )

        raise_oserror()


def test_logging_close_on_exception_filenotfounderror():
    with pytest.raises(FileNotFoundError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception-filenotfounderror.log',
            description=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def raise_filenotfounderror():
            errors.config.raise_exception(
                msg='',
                exception=errors.config.FileNotFoundError()
            )

        raise_filenotfounderror()


def test_logging_close_on_exception_typeerror():
    with pytest.raises(TypeError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception-typeerror.log',
            description=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def raise_typeerror():
            errors.config.raise_exception(
                msg='',
                exception=errors.config.TypeError()
            )

        raise_typeerror()


def test_logging_close_on_exception_validationerror():
    with pytest.raises(errors.config.ValidationError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception-validationerror.log',
            description=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def raise_validationerror():
            errors.config.raise_exception(
                msg='',
                exception=errors.config.ValidationError()
            )

        raise_validationerror()


def test_logging_close_on_exception_notimplementederror():
    with pytest.raises(NotImplementedError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception-notimplementederror.log',
            description=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def raise_notimplementederror():
            errors.config.raise_exception(
                msg='',
                exception=ValueError()
            )

        raise_notimplementederror()
