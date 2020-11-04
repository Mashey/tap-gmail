import vcr
import pytest
import pytest_vcr
from tap_gmail import *

def test_fetch_reports_gmail():
    x = 2
    assert x == 2


def test_for_circleci_env():
    x = 2 + 3
    assert x == 5

