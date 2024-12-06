
import pytest
from rangy.rangy import Rangy, EXACT, ANY, AT_LEAST_ONE, RANGE

@pytest.mark.parametrize("rangy, expected_type", [
    (4, EXACT),
    ("4", EXACT),
    ("*", ANY),
    ("+", AT_LEAST_ONE),
    ("1-3", RANGE),
    ((1, 3), RANGE),
    (("1", "3"), RANGE),
    (("4", "*"), RANGE),
], ids=[
    "int_exact",
    "str_exact",
    "any_count",
    "at_least_one",
    "range_str",
    "range_tuple_int",
    "range_tuple_str",
    "range_tuple_mixed"
])
def test_determine_type(rangy, expected_type):
    var_count = Rangy(rangy)
    assert var_count._determine_type() == expected_type