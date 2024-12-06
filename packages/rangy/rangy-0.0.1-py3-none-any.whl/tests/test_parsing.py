import pytest

from rangy import Rangy, ANY, AT_LEAST_ONE, EXACT, RANGE


def test_from_string_exact():
    count = Rangy("3")
    assert count._type == EXACT
    assert count.value == 3

def test_from_string_any():
    count = Rangy("*")
    assert count._type == ANY
    assert count.values == (0, 1000000)

def test_from_string_at_least_one():
    count = Rangy("+")
    assert count._type == AT_LEAST_ONE
    assert count.values == (1, 1000000)

def test_from_string_range():
    count = Rangy("1-3")
    assert count._type == RANGE
    assert count.values == (1, 3)

def test_from_string_range_lower_any():
    count = Rangy("*-3")
    assert count._type == RANGE
    assert count.values == (0, 3)

def test_from_string_range_lower_at_least_one():
    count = Rangy("+-3")
    assert count._type == RANGE
    assert count.values == (1, 3)

def test_from_string_range_upper_any():
    count = Rangy("3-*")
    assert count._type == RANGE
    assert count.values == (3, 1000000)

def test_from_string_range_upper_at_least_one():
    count = Rangy("3-+")
    assert count._type == RANGE
    assert count.values == (3, 1000000)

if __name__ == "__main__":
    pytest.main()
