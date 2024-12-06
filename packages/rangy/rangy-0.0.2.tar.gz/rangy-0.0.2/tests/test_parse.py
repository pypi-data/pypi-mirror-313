import pytest
from rangy import _parse, INFINITY

@pytest.mark.parametrize("count, expected", [
    (4, (4, 4)),
    ("4", (4, 4)),
    ("*", (0, INFINITY)),
    ("+", (1, INFINITY)),
    ("1-3", (1, 3)),
    ((1, 3), (1, 3)),
    (("1", "3"), (1, 3)),
    (("4", "*"), (4, INFINITY)),
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
    assert _parse(None, count) == expected

@pytest.mark.parametrize("count", [
    "invalid",
    (1, 2, 3),
    (1,),
    (None, 3),
    (3, None),
    (-1, 3),
    (3, -1),
    (-1, -3),
    "1-3-5",
    "1,3,5",
    "1:3:5",
    "1;3;5",
], ids=[
    "invalid_str",
    "invalid_tuple_three_elements",
    "invalid_tuple_one_element",
    "invalid_tuple_none_min",
    "invalid_tuple_none_max",
    "negative_min",
    "negative_max",
    "negative_both",
    "invalid_range_hyphen",
    "invalid_range_comma",
    "invalid_range_colon",
    "invalid_range_semicolon"
])
def test_parse_invalid(count):
    with pytest.raises(ValueError):
        _parse(None, count)