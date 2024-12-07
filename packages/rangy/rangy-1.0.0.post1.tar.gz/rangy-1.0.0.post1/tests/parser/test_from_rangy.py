import pytest

from rangy import parse_range, Rangy

def test_from_rangy():
    res = parse_range(Rangy((1, 3)))
    assert res == (1, 3)