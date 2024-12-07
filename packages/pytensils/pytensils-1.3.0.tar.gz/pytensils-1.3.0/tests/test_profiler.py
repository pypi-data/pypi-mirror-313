"""
Information
---------------------------------------------------------------------
Name        : test_profiler.py
Location    : ~/tests

Description
---------------------------------------------------------------------
Tests methods within `pytensils.profiler`.
"""

import time
from pytensils import profiler


@profiler.run_time
def test_run_time_success():
    time.sleep(1)
