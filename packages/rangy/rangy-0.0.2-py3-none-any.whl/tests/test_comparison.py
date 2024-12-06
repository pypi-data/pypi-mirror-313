import pytest
from rangy import Rangy

@pytest.mark.parametrize("count, other, expected", [
    (4, 5, True),
    (4, 4, False),
    (4, 3, False),
    ("1-3", 4, True),
    ("1-3", 3, False),
    ("1-3", 2, False),
], ids=[
    "exact_less_than",
    "exact_equal",
    "exact_greater_than",
    "range_less_than",
    "range_equal",
    "range_greater_than"
])
def test_lt(count, other, expected):
    var_count = Rangy(count)
    assert (var_count < other) == expected

@pytest.mark.parametrize("count, other, expected", [
    (4, 5, True),
    (4, 4, True),
    (4, 3, False),
    ("1-3", 4, True),
    ("1-3", 3, True),
    ("1-3", 2, False),
], ids=[
    "exact_less_than_or_equal",
    "exact_equal",
    "exact_greater_than",
    "range_less_than_or_equal",
    "range_equal",
    "range_greater_than"
])
def test_le(count, other, expected):
    var_count = Rangy(count)
    assert (var_count <= other) == expected

@pytest.mark.parametrize("count, other, expected", [
    (4, 3, True),
    (4, 4, False),
    (4, 5, False),
    ("1-3", 0, True),
    ("1-3", 1, False),
    ("1-3", 2, False),
], ids=[
    "exact_greater_than",
    "exact_equal",
    "exact_less_than",
    "range_greater_than",
    "range_equal",
    "range_less_than"
])
def test_gt(count, other, expected):
    var_count = Rangy(count)
    assert (var_count > other) == expected

@pytest.mark.parametrize("count, other, expected", [
    (4, 3, True),
    (4, 4, True),
    (4, 5, False),
    ("1-3", 0, True),
    ("1-3", 1, True),
    ("1-3", 2, False),
], ids=[
    "exact_greater_than_or_equal",
    "exact_equal",
    "exact_less_than",
    "range_greater_than_or_equal",
    "range_equal",
    "range_less_than"
])
def test_ge(count, other, expected):
    var_count = Rangy(count)
    assert (var_count >= other) == expected

@pytest.mark.parametrize("count", [
    (-1, 3),
    (3, -1),
    (-1, -3),
], ids=[
    "negative_min",
    "negative_max",
    "negative_both"
])
def test_negative(count):
    with pytest.raises(ValueError):
        Rangy(count)