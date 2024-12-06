import pytest
from rangy import Rangy, distribute
SEPERATOR = "--"


@pytest.mark.parametrize("items, rangys, expected", [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy(1), Rangy(4), Rangy(5)], [[1], [2, 3, 4, 5], [6, 7, 8, 9, 10]]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy(1), Rangy(3), Rangy("*")], [[1], [2, 3, 4], [5, 6, 7, 8, 9, 10]]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy("*"), Rangy(3), Rangy(1)], [[1, 2, 3, 4, 5, 6], [7, 8, 9], [10]]),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy(1), Rangy("2-4"), Rangy("*")], [[1], [2, 3, 4, 5], [ 6, 7, 8, 9, 10]]),

    ([1, 2, SEPERATOR, 3, 4, 5, 6, SEPERATOR, 7, 8, 9, 10], [Rangy("1-4"), Rangy("4-*"), Rangy("4-9")], [[1, 2], [3, 4, 5, 6], [7, 8, 9, 10]]),
    ([1, 2, SEPERATOR, 3, 4, 5, 6, SEPERATOR, 7, 8, 9, 10, 11], [Rangy("1-4"), Rangy("2-6"), Rangy("4-9")], [[1, 2], [3, 4, 5, 6], [7, 8, 9, 10, 11]]),


], ids=[
    "fixed_counts",
    "one_any_count",
    "one_any_count_first",
    "one_range_count",
    "separator",
    "separator_overflow"
])
def test_distribute(items, rangys, expected):
    assert distribute(items, rangys) == expected


@pytest.mark.parametrize("items, rangys", [
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy("1-4"), Rangy("3-5"), Rangy("4-9")]),
    ([1, 2, SEPERATOR, 3, 4, 5, SEPERATOR, 7, 8, 9, 10], [Rangy("1-4"), Rangy("4-*"), Rangy("4-9")]),
    ([1,2,3], [Rangy(1), Rangy(1), Rangy(1), Rangy(1)]),
], ids=[
    "too_few_items",
    "separator_mismatch",
    "too_manys"
])
def test_distribute_invalid(items, rangys):
    with pytest.raises(ValueError):
        distribute(items, rangys)


@pytest.mark.parametrize("items, rangys, expected", [
     ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy("1-4"), Rangy("3-5"), Rangy("+")], [[1, 2, 3, 4], [5, 6, 7, 8, 9], [10]]),
     ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [Rangy("1-4"), Rangy("+"), Rangy("3-5")], [[1, 2, 3, 4], [5], [6, 7, 8, 9, 10]]),
], ids=[
    "at_least_one",
    "at_least_one_overflow"
])
def test_distribute_at_least_one(items, rangys, expected):
    assert distribute(items, rangys) == expected

