import pytest

from rangy.exceptions import ParseRangeError
from rangy.parse import parse_range


def test_single_integer():
    assert parse_range(5) == (5, 5)
def test_open():
    assert parse_range((5, "*")) == (5,None)

def test_tuple_of_integers():
    assert parse_range((3, 7)) == (3, 7)

def test_list_of_integers():
    assert parse_range([2, 8]) == (2, 8)

def test_invalid_tuple_length():
    with pytest.raises(ParseRangeError):
        parse_range((1, 2, 3))

def test_invalid_list_length():
    with pytest.raises(ParseRangeError):
        parse_range([1, 2, 3])

def test_unsupported_type():
    with pytest.raises(ParseRangeError):
        parse_range({1, 2})

def test_tuple_of_strings():
    assert parse_range(("3", "7")) == (3, 7)


def test_mixed_tuple():
    assert parse_range((3, "7")) == (3, 7)
    assert parse_range(("3", 7)) == (3, 7)


def test_single_string():
    assert parse_range("5") == (5, 5)


def test_range_input():
    another_range = (10, 20)
    assert parse_range(another_range) == (10, 20)

def test_range_input_open():
    another_range = (10, "*")
    assert parse_range(another_range) == (10, None)