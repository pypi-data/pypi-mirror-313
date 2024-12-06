
import pytest
from rangy import Rangy as Rangy

@pytest.mark.parametrize("count, expected_value", [
    (4, 4),
    ("4", 4),
], ids=[
    "int_exact",
    "str_exact"
])
def test_value(count, expected_value):
    var_count = Rangy(count)
    assert var_count.value == expected_value

@pytest.mark.parametrize("count, expected_values", [
    ("1-3", (1, 3)),
    ((1, 3), (1, 3)),
    (("1", "3"), (1, 3)),
    (("4", "*"), (4, 1000000)),
], ids=[
    "range_str",
    "range_tuple_int",
    "range_tuple_str",
    "range_tuple_mixed"
])
def test_values(count, expected_values):
    var_count = Rangy(count)
    assert var_count.values == expected_values

@pytest.mark.parametrize("count", [
    "*",
    "+"
], ids=[
    "any_count",
    "at_least_one"
])
def test_value_error(count):
    var_count = Rangy(count)
    with pytest.raises(ValueError):
        _ = var_count.value

@pytest.mark.parametrize("count", [
    4,
    "4"
], ids=[
    "int_exact",
    "str_exact"
])
def test_values_error(count):
    var_count = Rangy(count)
    with pytest.raises(ValueError):
        _ = var_count.values