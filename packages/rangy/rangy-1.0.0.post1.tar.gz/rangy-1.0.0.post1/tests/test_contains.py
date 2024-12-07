import pytest

from rangy import Rangy
from rangy.exceptions import ParseRangeError


@pytest.mark.parametrize("count, item, expected", [
    (4, 4, True),
    (4, 3, False),
    ("1-3", 2, True),
    ("1-3", 4, False),
    ("*", 100, True),
    ("+", 0, False),
    ("+", 1, True),
], ids=[
    "exact_contains",
    "exact_not_contains",
    "range_contains",
    "range_not_contains",
    "any_contains",
    "at_least_one_not_contains",
    "at_least_one_contains"
])
def test_contains(count, item, expected):
    var_count = Rangy(count)
    assert (item in var_count) == expected

@pytest.mark.parametrize("count", [
    (None, 3),
    (3, None),
], ids=[
    "none_min",
    "none_max"
])
def test_invalid_tuple(count):
    with pytest.raises(ParseRangeError):
        Rangy(count)

def test_validate_exact():
    count = Rangy(3)
    assert 3 in count
    assert 4 not in count

def test_validate_any():
    count = Rangy("*")
    assert 0 in count
    assert 1000 in count

def test_validate_at_least_one():
    count = Rangy("+")
    assert 1 in count
    assert 0 not in count

def test_validate_range():
    count = Rangy("1-3")
    assert 1 in count
    assert 2 in count
    assert 3 in count
    assert 0 not in count
    assert 4 not in count

def test_validate_range_lower_any():
    count = Rangy("*-3")
    assert 0 in count
    assert 1 in count
    assert 2 in count
    assert 3 in count
    assert 4 not in count

def test_validate_range_lower_at_least_one():
    count = Rangy("+-3")
    assert 1 in count
    assert 2 in count
    assert 3 in count
    assert 0 not in count
    assert 4 not in count

def test_validate_range_upper_any():
    count = Rangy("3-*")
    assert 3 in count
    assert 4 in count
    assert 1000 in count
    assert 2 not in count

def test_validate_range_upper_at_least_one():
    count = Rangy("3-+")
    assert 3 in count
    assert 4 in count
    assert 1000 in count
    assert 2 not in count

