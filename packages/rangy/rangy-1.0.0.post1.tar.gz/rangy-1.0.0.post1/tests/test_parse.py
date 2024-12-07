import pytest

from rangy import INFINITY
from rangy.parse  import parse_range

from rangy.exceptions import ParseRangeError


@pytest.mark.parametrize("count, expected", [
    (4, (4, 4)),
    ("4", (4, 4)),
    ("*", (0, None)),
    ("+", (1, None)),
    ("1-3", (1, 3)),
    ((1, 3), (1, 3)),
    (("1", "3"), (1, 3)),
    (("4", "*"), (4, None)),
    ("1,3", (1, 3)),
    ("1:3", (1, 3)),
    ("1;3", (1, 3)),
], ids=[
    "int_exact",
    "str_exact",
    "any_count",
    "at_least_one",
    "range_str",
    "range_tuple_int",
    "range_tuple_str",
    "range_tuple_mixed",
    "range_comma",
    "range_colon",
    "range_semicolon"
])
def test_parse(count, expected):
    parsed = parse_range(count)
    assert expected == parsed

@pytest.mark.parametrize("count", [
    "invalid",
    (1, 2, 3),
    (None, 3),
    (3, None),
    "1-3-5",
    "1,3,5",
    "1:3:5",
    "1;3;5",
], ids=[
    "invalid_str",
    "invalid_tuple_three_elements",
    "invalid_tuple_none_min",
    "invalid_tuple_none_max",
    "invalid_range_hyphen:triplet",
    "invalid_range_comma:triplet",
    "invalid_range_colon:triplet",
    "invalid_range_semicolon:triplet"
])
def test_parse_invalid(count):
    with pytest.raises(ParseRangeError):
        parse_range(count)