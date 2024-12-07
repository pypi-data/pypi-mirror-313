""" Directory and data-type utilities """

import os
import ast
import json
import datetime
from typing import Union
from typing_extensions import Literal


# Directory management function(s)
def generate_output_directory(
    path: str,
    root: str,
    sub_folders: Union[list, None] = None
):
    """ Generates an output directory with subfolders.

    Parameters
    ----------
    path : `str`
        Directory path to the folder that will contain the output folder
            directories.
    root : `str`
        The name of the root folder of the directory to create within `path`.
    sub_folders: `list`
        A list of folders to create within ~/`path`/`root`
    """

    if root not in os.listdir(path):

        # Create root output directory
        os.mkdir(os.path.join(path, root))

        # Create output sub-directories
        if sub_folders:
            for folder in sub_folders:
                os.mkdir(os.path.join(path, root, folder))
    else:
        raise OSError(
            '{~/%s} already exists.' % (root)
        )


# Data-type parsing function(s)
def as_type(
    value: str,
    return_dtype: Literal[
        'none',
        'str',
        'int',
        'float',
        'bool',
        'list',
        'dict',
        'datetime',
        'timedelta'
    ] = 'str'
) -> Union[
    str,
    int,
    float,
    bool,
    list,
    dict,
    datetime.datetime,
    datetime.timedelta
]:
    """ Returns `value` as `return_dtype`.

    Parameters
    ----------
    value : `str`
        String of the value to convert to `return_dtype`.
    return_dtype : `str`
        Name of the datatype of the returned value. If the returned value
            cannot be converted to `return_dtype` then a `TypeError` is
            raised. If the name of the `return_dtype` is invalid, then
            a `NameError` is returned.
    """

    try:
        if (
            return_dtype.strip().upper() == 'NONE'
            and not ast.literal_eval(value)
        ):
            return None

        if return_dtype.strip().upper() == 'STR':
            return str(value)

        elif return_dtype.strip().upper() == 'INT':
            return int(value)

        elif return_dtype.strip().upper() == 'FLOAT':
            return float(value)

        elif return_dtype.strip().upper() == 'BOOL':

            try:
                return ast.literal_eval(value)
            except (SyntaxError, ValueError):
                raise TypeError(
                    ' '.join([
                        "{%s} value" % (
                            value
                        ),
                        "cannot be converted to {%s}." % (
                            return_dtype
                        )
                    ])
                )

        elif return_dtype.strip().upper() == 'DATETIME':
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        elif return_dtype.strip().upper() == 'TIMEDELTA':
            return datetime.timedelta(seconds=float(value))

        elif (
            (return_dtype.strip().upper() == 'LIST')
            or (return_dtype.strip().upper() == 'DICT')
        ):
            try:
                return json.loads(value)
            except json.decoder.JSONDecodeError:
                raise TypeError(
                    ' '.join([
                        "{%s} value" % (
                            value
                        ),
                        "cannot be converted to {%s}." % (
                            return_dtype
                        )
                    ])
                )
        else:
            raise NameError(
                'Invalid return datatype {%s}.' % (
                    return_dtype
                )
            )
    except ValueError:
        raise TypeError(
            ' '.join([
                "{%s} value" % (
                    value
                ),
                "cannot be converted to {%s}." % (
                    return_dtype
                )
            ])
        )
