import pytest

from rangy  import Rangy, EXACT, ANY, AT_LEAST_ONE, RANGE

def test_validate_exact():
    count = Rangy(3)
    assert count.validate(3)
    assert not count.validate(4)

def test_validate_any():
    count = Rangy("*")
    assert count.validate(0)
    assert count.validate(1000)

def test_validate_at_least_one():
    count = Rangy("+")
    assert count.validate(1)
    assert not count.validate(0)

def test_validate_range():
    count = Rangy("1-3")
    assert count.validate(1)
    assert count.validate(2)
    assert count.validate(3)
    assert not count.validate(0)
    assert not count.validate(4)

def test_validate_range_lower_any():
    count = Rangy("*-3")
    assert count.validate(0)
    assert count.validate(1)
    assert count.validate(2)
    assert count.validate(3)
    assert not count.validate(4)

def test_validate_range_lower_at_least_one():
    count = Rangy("+-3")
    assert count.validate(1)
    assert count.validate(2)
    assert count.validate(3)
    assert not count.validate(0)
    assert not count.validate(4)

def test_validate_range_upper_any():
    count = Rangy("3-*")
    assert count.validate(3)
    assert count.validate(4)
    assert count.validate(1000)
    assert not count.validate(2)

def test_validate_range_upper_at_least_one():
    count = Rangy("3-+")
    assert count.validate(3)
    assert count.validate(4)
    assert count.validate(1000)
    assert not count.validate(2)

if __name__ == "__main__":
    pytest.main()
