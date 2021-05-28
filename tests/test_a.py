"""
Mock first test
"""
from assertpy import assert_that
import time

def test_one():
    assert_that(1).is_equal_to(1)

def test_two():
    assert_that(2).is_equal_to(2)
    time.sleep(5)
