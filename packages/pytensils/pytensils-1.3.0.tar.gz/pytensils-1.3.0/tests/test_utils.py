"""
Information
---------------------------------------------------------------------
Name        : test_utils.py
Location    : ~/tests

Description
---------------------------------------------------------------------
Tests methods within `pytensils.utils`.
"""

import os
import pytest
from pytensils import utils


def test_generate_output_directory_success(tmp_path):
    utils.generate_output_directory(
        path=tmp_path,
        root='root',
        sub_folders=['A', 'B', 'C']
    )
    assert os.path.isdir(os.path.join(tmp_path, 'root'))
    assert os.path.isdir(os.path.join(tmp_path, 'root', 'A'))
    assert os.path.isdir(os.path.join(tmp_path, 'root', 'B'))
    assert os.path.isdir(os.path.join(tmp_path, 'root', 'C'))


def test_generate_output_directory_oserror():
    with pytest.raises(OSError):
        utils.generate_output_directory(
            path=os.path.abspath(
                os.path.dirname(__file__)
            ),
            root='resources'
        )


def test_as_type_success_none():
    assert not utils.as_type(value='None', return_dtype='none')


def test_as_type_success_str():
    assert utils.as_type(value='ABC') == 'ABC'


def test_as_type_success_int():
    assert utils.as_type(value='1', return_dtype='int') == 1


def test_as_type_success_float():
    assert utils.as_type(value='9.9', return_dtype='float') == 9.9


def test_as_type_success_bool():
    assert utils.as_type(value='True', return_dtype='bool')


def test_as_type_success_datetime():
    assert utils.as_type(
        value='2024-07-08 18:11:00',
        return_dtype='datetime'
    )


def test_as_type_success_timedelta():
    assert utils.as_type(value='3600', return_dtype='timedelta')


def test_as_type_success_list():
    assert utils.as_type(
        value='["A", "B", "C"]',
        return_dtype='list'
    ) == ['A', 'B', 'C']


def test_as_type_success_dict():
    assert utils.as_type(
        value='{"A": "a", "B": "b", "C": "c"}',
        return_dtype='dict'
    ) == {
        'A': "a",
        'B': 'b',
        'C': 'c'
    }


def test_as_type_failure_typeerror():
    with pytest.raises(TypeError):
        utils.as_type(
            value='FALSE',
            return_dtype='bool'
        )


def test_as_type_failure_jsondecoder():
    with pytest.raises(TypeError):
        utils.as_type(
            value='{"A": "a", "B"="b", "C": "c"}',
            return_dtype='dict'
        )


def test_as_type_failure_nameerror():
    with pytest.raises(NameError):
        utils.as_type(
            value='ABC',
            return_dtype='string'
        )


def test_as_type_failure_typeerror_general():
    with pytest.raises(TypeError):
        utils.as_type(
            value='ABC',
            return_dtype='int'
        )
