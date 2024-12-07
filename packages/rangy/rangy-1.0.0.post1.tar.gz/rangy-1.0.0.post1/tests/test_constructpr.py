import pytest

from rangy import ANY, AT_LEAST_ONE, EXACT, RANGE, Rangy


def test_from_string_exact():
    count = Rangy("3")
    assert count.value == 3

def test_from_string_any():
    count = Rangy("*")

    assert count.values == (0, None)

def test_from_string_at_least_one():
    count = Rangy("+")
    assert count.values == (1, None)

def test_from_string_range():
    count = Rangy("1-3")
    assert count.values == (1, 3)

def test_from_string_range_lower_any():
    count = Rangy("*-3")
    assert count.values == (0, 3)

def test_from_string_range_lower_at_least_one():
    count = Rangy("+-3")
    assert count.values == (1, 3)

def test_from_string_range_upper_any():
    count = Rangy("3-*")
    assert count.values == (3, None)

def test_from_string_range_upper_at_least_one():
    count = Rangy("3-+")
    assert count.values == (3, None)

if __name__ == "__main__":
    pytest.main()
