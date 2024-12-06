import pytest
from rangy import Rangy

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
    with pytest.raises(ValueError):
        Rangy(count)