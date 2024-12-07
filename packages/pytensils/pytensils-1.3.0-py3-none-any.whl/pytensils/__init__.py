""" pytensils

A Python package that provides general utility functions for managing
configuration, user-logging, directories and data-types as well as
a basic run-time profiler.
"""

import pytensils.config as config
import pytensils.logging as logging
import pytensils.utils as utils
import pytensils.profiler as profiler
import pytensils.errors as errors

__name__ = 'pytensils'
__all__ = ['config', 'logging', 'utils', 'profiler', 'errors']
