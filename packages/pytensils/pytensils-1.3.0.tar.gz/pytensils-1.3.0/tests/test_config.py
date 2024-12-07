"""
Information
---------------------------------------------------------------------
Name        : test_config.py
Location    : ~/tests

Description
---------------------------------------------------------------------
Tests methods within `pytensils.config`.
"""

import os
import pytest
from pytensils import config, logging, errors

PATH = os.path.join(
    os.path.dirname(__file__),
    'resources'
)


@pytest.fixture
def CONFIG_FIXTURE() -> config.Handler:
    return config.Handler(
        path=PATH,
        file_name='config.json'
    )


@pytest.fixture
def DTYPES_FIXTURE() -> config.Handler:
    return config.Handler(
        path=PATH,
        file_name='dtypes.json'
    )


@pytest.fixture
def CONFIG_VALIDATION_ERROR_FIXTURE() -> config.Handler:
    return config.Handler(
        path=PATH,
        file_name='config_validation_error.json'
    )


@pytest.fixture
def LOGGING_FIXTURE() -> logging.Handler:
    return logging.Handler(
        path=PATH,
        file_name='test_config.log'
    )


@pytest.fixture
def CONFIG_FIXTURE_WITH_LOGGING(
    LOGGING_FIXTURE: logging.Handler
) -> config.Handler:
    return config.Handler(
        path=PATH,
        file_name='config.json',
        Logging=LOGGING_FIXTURE
    )


@pytest.fixture
def CONFIG_VALIDATION_ERROR_FIXTURE_WITH_LOGGING(
    LOGGING_FIXTURE: logging.Handler
) -> config.Handler:
    return config.Handler(
        path=PATH,
        file_name='config_validation_error.json',
        Logging=LOGGING_FIXTURE
    )


def test_init_success(CONFIG_FIXTURE: config.Handler):
    assert CONFIG_FIXTURE.path == PATH
    assert CONFIG_FIXTURE.file_name == 'config.json'
    assert CONFIG_FIXTURE.data == {
        "config": {
            "str": "ABC",
            "bool": True,
            "int": 1,
            "float": 9.9,
            "list": ["A", "B", "C"]
        }
    }
    assert not CONFIG_FIXTURE.validation_errors


def test_init_oserror():
    with pytest.raises(OSError):
        _ = config.Handler(
            path=os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)
                ),
                'path-does-not-exist'
            )
        )


def test_init_logging_oserror(LOGGING_FIXTURE: logging.Handler):
    with pytest.raises(OSError):
        _ = config.Handler(
            path=os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)
                ),
                'path-does-not-exist'
            ),
            Logging=LOGGING_FIXTURE
        )


def test_init_filenotfounderror():
    with pytest.raises(FileNotFoundError):
        _ = config.Handler(
            path=PATH,
            file_name='file-not-found.json'
        )


def test_init_logging_filenotfounderror(
    LOGGING_FIXTURE: logging.Handler
):
    with pytest.raises(FileNotFoundError):
        _ = config.Handler(
            path=PATH,
            file_name='file-not-found.json',
            Logging=LOGGING_FIXTURE
        )


def test_read_success(CONFIG_FIXTURE: config.Handler):
    assert CONFIG_FIXTURE.read() == {
        "config": {
            "str": "ABC",
            "bool": True,
            "int": 1,
            "float": 9.9,
            "list": ["A", "B", "C"]
        }
    }


def test_read_typeerror():
    with pytest.raises(TypeError):
        _ = config.Handler(
            path=PATH,
            file_name='config_invalid.json'
        )


def test_read_logging_typeerror(
    LOGGING_FIXTURE: logging.Handler
):
    with pytest.raises(TypeError):
        _ = config.Handler(
            path=PATH,
            file_name='config_invalid.json',
            Logging=LOGGING_FIXTURE
        )


def test_to_dict_success(CONFIG_FIXTURE: config.Handler):
    assert CONFIG_FIXTURE.to_dict() == {
        "config": {
            "str": "ABC",
            "bool": True,
            "int": 1,
            "float": 9.9,
            "list": ["A", "B", "C"]
        }
    }


def test_from_dict_success(
    CONFIG_FIXTURE: config.Handler,
    DTYPES_FIXTURE: config.Handler
):
    assert CONFIG_FIXTURE == CONFIG_FIXTURE.from_dict(
        dict_object={
            "config": {
                "str": "ABC",
                "bool": True,
                "int": 1,
                "float": 9.9,
                "list": ["A", "B", "C"]
            }
        },
        dtypes=DTYPES_FIXTURE.to_dict()
    )
    assert CONFIG_FIXTURE.data == {
        "config": {
            "str": "ABC",
            "bool": True,
            "int": 1,
            "float": 9.9,
            "list": ["A", "B", "C"]
        }
    }


def test_validate_from_dict_success(
    CONFIG_FIXTURE: config.Handler,
    DTYPES_FIXTURE: config.Handler
):
    assert CONFIG_FIXTURE.validate(
        dtypes=DTYPES_FIXTURE.to_dict()
    )
    assert not CONFIG_FIXTURE.validation_errors


def test_validate_from_config_handler_success(
    CONFIG_FIXTURE: config.Handler,
    DTYPES_FIXTURE: config.Handler
):
    assert CONFIG_FIXTURE.validate(
        dtypes=DTYPES_FIXTURE
    )
    assert not CONFIG_FIXTURE.validation_errors


def test_validate_assertionerror(
    CONFIG_FIXTURE: config.Handler
):
    with pytest.raises(AssertionError):
        CONFIG_FIXTURE.validate(
            dtypes='invalid-type'
        )


def test_validate_instance_validationerror(CONFIG_FIXTURE: config.Handler):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_FIXTURE._validate_instance(
            dict_object=['A', 'B', 'C"'],
            parameter='invalid-instance-dict-object'
        )


def test_validate_instance_logging_validationerror(
    CONFIG_FIXTURE_WITH_LOGGING: config.Handler
):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_FIXTURE_WITH_LOGGING._validate_instance(
            dict_object=['A', 'B', 'C"'],
            parameter='invalid-instance-dict-object'
        )


def test_validate_data_validationerror(CONFIG_FIXTURE: config.Handler):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_FIXTURE._validate_data(
            dict_object={},
            parameter='empty-dict-object'
        )


def test_validate_data_logging_validationerror(
    CONFIG_FIXTURE_WITH_LOGGING: config.Handler
):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_FIXTURE_WITH_LOGGING._validate_data(
            dict_object={},
            parameter='empty-dict-object'
        )


def test_validate_depth_validationerror(CONFIG_FIXTURE: config.Handler):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_FIXTURE._validate_depth(
            dict_object={'A': 'str'},
            parameter='invalid-depth-dict-object'
        )


def test_validate_depth_logging_validationerror(
    CONFIG_FIXTURE_WITH_LOGGING: config.Handler
):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_FIXTURE_WITH_LOGGING._validate_depth(
            dict_object={'A': 'str'},
            parameter='invalid-depth-dict-object'
        )


def test_validate_dtypes_validationerror(
    CONFIG_VALIDATION_ERROR_FIXTURE: config.Handler,
    DTYPES_FIXTURE: config.Handler
):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_VALIDATION_ERROR_FIXTURE.validate(
            dtypes=DTYPES_FIXTURE.to_dict()
        )


def test_validate_dtypes_logging_validationerror(
    CONFIG_VALIDATION_ERROR_FIXTURE_WITH_LOGGING: config.Handler,
    DTYPES_FIXTURE: config.Handler
):
    with pytest.raises(errors.config.ValidationError):
        CONFIG_VALIDATION_ERROR_FIXTURE_WITH_LOGGING.validate(
            dtypes=DTYPES_FIXTURE.to_dict()
        )


def test_write_success(tmp_path):

    # Create an empty config-file
    with open(os.path.join(tmp_path, 'config_temp.json'), 'w'):
        pass

    # Output content to the config-file
    temp = config.Handler(
        path=tmp_path,
        file_name='config_temp.json',
        create=True
    )
    temp.from_dict(
        dict_object={
            "config": {
                "str": "ABC",
                "bool": True,
                "int": 1,
                "float": 9.9,
                "list": ["A", "B", "C"]
            }
        }
    )
    assert temp.to_dict() == {
        "config": {
            "str": "ABC",
            "bool": True,
            "int": 1,
            "float": 9.9,
            "list": ["A", "B", "C"]
        }
    }
