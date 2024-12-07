import pytest

from rangy.exceptions import ParseRangeError
from rangy import parse_range
from rangy.parse import _nomalize_str


def test_str_single_integer():
    assert parse_range("5") == (5, 5)

def test_normalize_str_basic():
    assert _nomalize_str("1-5") == ("1", "5")
    assert _nomalize_str("(1-5)") == ("1", "5")
    assert _nomalize_str("[1-5]") == ("1", "5")

def test_normalize_str_with_spaces():
    assert _nomalize_str(" 1 - 5 ") == ("1", "5")
    assert _nomalize_str("[ 1 - 5 ]") == ("1", "5")
    assert _nomalize_str("( 1 - 5 )") == ("1", "5")

def test_normalize_str_with_commas():
    assert _nomalize_str("1,5") == ("1", "5")
    assert _nomalize_str("(1,5)") == ("1", "5")
    assert _nomalize_str("[1,5]") == ("1", "5")

def test_normalize_str_with_semicolons():
    assert _nomalize_str("1;5") == ("1", "5")
    assert _nomalize_str("(1;5)") == ("1", "5")
    assert _nomalize_str("[1;5]") == ("1", "5")

def test_normalize_str_single_value():
    assert _nomalize_str("5") == ("5",)
    assert _nomalize_str("(5)") == ("5",)
    assert _nomalize_str("[5]") == ("5",)

