""" Configuration management """

from __future__ import annotations
import os
import json
import copy
import pandas as pd
from typing import Union, Tuple
from pytensils import logging, errors

# Private static variable(s)
_MIN_DEPTH = 2


class Handler():
    """ A `class` that represents a configuration-handler.

    Parameters
    ----------
    path : `str`
        Directory path to the folder that contains the `file_name` of the
            '.json' config-file.
    file_name : `str`
        File name of the '.json' config-file.
    create: `bool`
        `True` or `False`, creates an empty log-file, `file_name`
            within `path` when `True`.
    Logging: `pytensils.logging.Handler`
        An instance of the `pytensils.logging.Handler` class that allows
            for native 'pretty' user-logging of all `ValidationError`
            exceptions.
    """

    def __init__(
        self,
        path: str,
        file_name: str = 'config.json',
        create: bool = False,
        Logging: Union[logging.Handler, None] = None
    ):
        """ Initializes an instance of the configuration-handler class.

        Parameters
        ----------
        path : `str`
            Directory path to the folder that contains the `file_name` of the
                '.json' config-file.
        file_name : `str`
            File name of the '.json' config-file.
        create: `bool`
            `True` or `False`, creates an empty log-file, `file_name`
                within `path` when `True`.
        Logging: `pytensils.logging.Handler`
            An instance of the `pytensils.logging.Handler` class that allows
                for native 'pretty' user-logging of all `ValidationError`
                exceptions.
        """

        # Assign class variables
        self.path = path
        self.file_name = file_name
        self.data = {}
        self.validation_errors = None

        # Assign private variables
        self._LOGGING = Logging

        # Validate the file-path
        if not os.path.isdir(path):
            if self._LOGGING:

                # Logging
                self._LOGGING.write_header(
                    header='Configuration validation'
                )
                self._LOGGING.write(
                    content='{%s} does not exist.' % (path),
                    level='ERROR'
                )
                self._LOGGING.close()
                raise errors.config.OSError(
                    'Path not found. See {%s} for more information.' % (
                        os.path.join(
                            self._LOGGING.path,
                            self._LOGGING.file_name
                        )
                    )
                )
            else:
                raise errors.config.OSError(
                    '{%s} does not exist.' % (path)
                )

        # Validate the file-name
        if not create:
            if os.path.isfile(
                os.path.join(path, file_name)
            ):
                self.data = self.read()

            else:
                if self._LOGGING:

                    # Logging
                    self._LOGGING.write_header(
                        header='Configuration validation'
                    )
                    self._LOGGING.write(
                        content='{%s} does not exist within {%s}.' % (
                            file_name,
                            path
                        ),
                        level='ERROR'
                    )
                    self._LOGGING.close()

                    # Raise exception
                    raise errors.config.FileNotFoundError(
                        'File not found. See {%s} for more information.' % (
                            os.path.join(
                                self._LOGGING.path,
                                self._LOGGING.file_name
                            )
                        )
                    )
                else:
                    raise errors.config.FileNotFoundError(
                        '{%s} does not exist within {%s}.' % (
                            file_name,
                            path
                        )
                    )

    def read(self) -> dict:
        """ Reads a '.json' config-file, updates the config data
        and returns the content as a `dict`.
        """
        with open(
            os.path.join(
                self.path,
                self.file_name
            ),
            mode='r'
        ) as file:
            try:

                # Load `.json` config-file
                dict_object = json.load(file)

                # Validate instance
                self._validate_instance(
                    dict_object=dict_object,
                    parameter=os.path.join(
                        self.path,
                        self.file_name
                    )
                )

                # Validate data
                self._validate_data(
                    dict_object=dict_object,
                    parameter=os.path.join(
                        self.path,
                        self.file_name
                    )
                )

                # Validate depth
                self._validate_depth(
                    dict_object=dict_object,
                    parameter=os.path.join(
                        self.path,
                        self.file_name
                    )
                )

                # Update the config data
                self.data = copy.deepcopy(dict_object)

                return dict_object

            except json.decoder.JSONDecodeError:
                if self._LOGGING:

                    # Logging
                    self._LOGGING.write_header(
                        header='Configuration validation'
                    )
                    self._LOGGING.write(
                        content="{%s} is not a valid '.json' config-file." % (
                            self.file_name
                        ),
                        level='ERROR'
                    )
                    self._LOGGING.close()

                    # Raise exception
                    raise errors.config.TypeError(
                        ''.join([
                            'Invalid config-file format.',
                            ' See {%s} for more information.' % (
                                os.path.join(
                                    self._LOGGING.path,
                                    self._LOGGING.file_name
                                )
                            )
                        ])
                    )
                else:
                    raise errors.config.TypeError(
                        "{%s} is not a valid '.json' config-file." % (
                            self.file_name
                        )
                    )

    def write(self):
        """ Writes a '.json' config-file. """
        with open(
            os.path.join(
                self.path,
                self.file_name
            ),
            mode='w+'
        ) as file:
            json.dump(
                self.data,
                file,
                indent=4
            )

    def validate(
        self,
        dtypes: Union[dict, Handler],
    ) -> bool:
        """ Validates the config-file data against the dtypes in `dtypes`.
        Returns `True` when validation completes successfully.

        Parameters
        ----------
        dtypes : Union[`dict`, `pytensils.config.Handler`]
            Dictionary object that contains the expected
                configuration value dtypes.
        """
        assert type(dtypes) in [dict, Handler], (
            ''.join([
                '{dtypes} must be either a `dict` or an instance of',
                ' `pytensils.config.Handler`.'
            ])
        )

        # Parse the config data as a dictionary
        if isinstance(dtypes, Handler):
            dtypes = dtypes.to_dict()

        # Validate instance
        self._validate_instance(dict_object=dtypes, parameter='dtypes')

        # Validate data
        self._validate_data(dict_object=dtypes, parameter='dtypes')

        # Validate depth
        self._validate_depth(dict_object=dtypes, parameter='dtypes')

        # Validate dtypes
        self._validate_dtypes(
            dict_object=copy.deepcopy(self.data),
            dtype_object=dtypes
        )

        # Set validation error status
        self.validation_errors = None

        return True

    def to_dict(self) -> dict:
        """ Returns a dictionary object of the config-file data. """
        return copy.deepcopy(self.data)

    def from_dict(
        self,
        dict_object: dict,
        dtypes: Union[dict, None] = None
    ):
        """ Updates the config-file data with the contents of `dict_object`
        and validates the configuration against `dtypes` when
        `dtypes` is not None.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object containing configuration values.
        dtypes : `dict`
            Dictionary object that contains the expected
                configuration value dtypes.
        """

        # Validate instance
        self._validate_instance(
            dict_object=dict_object,
            parameter='dict_object'
        )

        # Validate data
        self._validate_data(
            dict_object=dict_object,
            parameter='dict_object'
        )

        # Validate depth
        self._validate_depth(
            dict_object=dict_object,
            parameter='dict_object'
        )

        if dtypes:

            # Validate instance
            self._validate_instance(dict_object=dtypes, parameter='dtypes')

            # Validate data
            self._validate_data(dict_object=dtypes, parameter='dtypes')

            # Validate depth
            self._validate_depth(dict_object=dtypes, parameter='dtypes')

            # Validate dtypes
            self._validate_dtypes(dict_object=dict_object, dtype_object=dtypes)

        # Retain configuration data
        self.data = copy.deepcopy(dict_object)

        # Write configuration data
        self.write()

        return self

    def _validate_instance(
        self,
        dict_object: dict,
        parameter: str
    ):
        """ Validates the type instance of `dict_object`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object to validate.
        parameter : 'str'
            The name of the parameter to report in the error message.
        """
        error_msg = 'Invalid data type {%s} for {%s}. Expected {dict}.' % (
            type(dict_object).__name__,
            parameter
        )

        if not isinstance(dict_object, dict):
            if self._LOGGING:
                self._raise_general_validation_error(error_msg=error_msg)
            raise errors.config.ValidationError(error_msg)

    def _validate_data(
        self,
        dict_object: dict,
        parameter: str
    ):
        """ Validates the data in `dict_object`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object to validate.
        parameter : `dict`
            The name of the parameter to report in the error message.
        """
        error_msg = '{%s} is empty.' % (
            parameter
        )

        if not dict_object:
            if self._LOGGING:
                self._raise_general_validation_error(error_msg=error_msg)
            else:
                raise errors.config.ValidationError(error_msg)

    def _validate_depth(
        self,
        dict_object: dict,
        parameter: str
    ):
        """ Validates the depth of `dict_object`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object to validate.
        """
        error_msg = ''.join([
            'The parameter {%s} must be a dictionary of' % (
                parameter
            ),
            ' dictionaries with a minimum depth of {%s}.' % (
                _MIN_DEPTH
            )
        ])

        if not logging._return_dictionary_depth(
            dict_object=dict_object
        ) >= _MIN_DEPTH:
            if self._LOGGING:
                self._raise_general_validation_error(error_msg=error_msg)
            else:
                raise errors.config.ValidationError(error_msg)

    def _validate_dtypes(
        self,
        dict_object: dict,
        dtype_object: dict
    ):
        """ Validates `dict_object` against the dtypes in `dtype_object`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object containing configuration values.
        dtype_object : `dict`
            Dictionary object that contains the expected
                configuration value dtypes.
        """
        error_msg = ''.join([
            'Validation failed. The following parameter values',
            ' are inconsistent with the expected data-types.'
        ])

        # Parse configuration dtype errors
        error, dtype_errors = self._parse_dtype_errors_to_dict(
            dict_object=dict_object,
            dtype_object=dtype_object
        )

        # Retain configuration dtype errors
        if error:
            self.validation_errors = copy.deepcopy(dtype_errors)

            # Raise configuration dtype errors
            if self._LOGGING:
                self._raise_dtype_validation_error(error_msg=error_msg)
            else:
                raise errors.config.ValidationError(
                    ''.join([
                        error_msg,
                        '\n%s' % (
                            json.dumps(dtype_errors, indent=2)
                        )
                    ])
                )

        else:
            self.validation_errors = None

    def _raise_general_validation_error(
        self,
        error_msg: str
    ):
        """ Reports an error string to `logging.Handler` and raises
        a `ValidationError`.
        """
        # Logging
        self._LOGGING.write_header(
            header='Configuration validation'
        )
        self._LOGGING.write(
            content=error_msg,
            level='ERROR'
        )
        self._LOGGING.close()

        # Raise exception
        raise errors.config.ValidationError(
            ''.join([
                'Validation failed.',
                ' See {%s} for more information.' % (
                    os.path.join(
                        self._LOGGING.path,
                        self._LOGGING.file_name
                    )
                )
            ])
        )

    def _raise_dtype_validation_error(
        self,
        error_msg: str
    ):
        """ Reports an error string and all invalid configuration parameters
        to `logging.Handler` and raises a `ValidationError`.
        """

        # Logging
        self._LOGGING.write_header(
            header='Configuration validation'
        )
        self._LOGGING.write(
            content=error_msg,
            level='ERROR'
        )
        self._LOGGING.write(
            content=self._convert_dtype_errors_to_df(
                dict_object=self.validation_errors
            )
        )
        self._LOGGING.close()

        # Raise exception
        raise errors.config.ValidationError(
            ''.join([
                'Validation failed.',
                ' See {%s} for more information.' % (
                    os.path.join(
                        self._LOGGING.path,
                        self._LOGGING.file_name
                    )
                )
            ])
        )

    def _parse_dtype_errors_to_dict(
        self,
        dict_object: dict,
        dtype_object: dict
    ) -> Tuple[bool, dict]:
        """ Returns the contents of the validation-error dictionary as
        a `pd.DataFrame`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object to parse.
        dtype_object : `dict`
            Dictionary object that contains the expected
                configuration value dtypes.
        """
        dtype_errors = {}
        error = False
        for section in dict_object.keys():
            if section not in dtype_object.keys():
                dtype_object[section] = {}
                dtype_errors[section] = {
                    '-N/A-': 'No corresponding section found in {dtypes}.'
                }
            else:
                dtype_errors[section] = {}

            for key, value in dict_object[section].items():
                if key not in dtype_object[section].keys():
                    dtype_errors[section][key] = (
                        'No dtype found in {dtypes}.'
                    )
                    error = True
                else:
                    if type(value).__name__ != dtype_object[section][key]:
                        dtype_errors[section][key] = (
                            'Invalid dtype {%s}. Expected {%s}.' % (
                                type(value).__name__,
                                dtype_object[section][key]
                            )
                        )
                        error = True
                    else:
                        pass

        return (error, dtype_errors)

    def _convert_dtype_errors_to_df(
        self,
        dict_object: dict
    ) -> pd.DataFrame:
        """ Returns the contents of the validation-error dictionary as
        a `pd.DataFrame`.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary object to convert.
        """
        df = pd.DataFrame()
        for key in dict_object.keys():
            df = pd.concat(
                [
                    df,
                    pd.DataFrame.from_dict(
                        {
                            'Section': [key] * len(
                                dict_object[key].values()
                            ),
                            'Key': dict_object[key].keys(),
                            'Error': dict_object[key].values()
                        }
                    )
                ],
                axis=0,
                ignore_index=True
            )

        return df
