""" Run-time profiling """

import time
import datetime as dt
from typing import Callable


# Decorator function(s)
def run_time(
    func: Callable
) -> Callable:
    """ Prints the run time of the {func} passed.

    Parameters
    ----------
    func : `Callable`
        Function object.
    """

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        td = dt.timedelta(seconds=(t2-t1))
        print("\n[INFO] Function {%s()} executed in %s hh:mm:ss." % (
                func.__name__,
                td
            )
        )
        return result
    return wrapper
