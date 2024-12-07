import pytest
from datetime import date
from rangy.builtins import DateConverter
from rangy import parse_range, Rangy
from rangy.registry import ConverterRegistry
from tests.fixtures.register import register_converters


@pytest.mark.usefixtures("register_converters")
def test_date_rangy():
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    res = parse_range(Rangy((start_date, end_date)))
    assert res == (start_date.toordinal(), end_date.toordinal())

@pytest.mark.usefixtures("register_converters")
def test_singular_date_rangy():
    singular_date = date(2023, 6, 15)
    rangy_obj = Rangy((singular_date, singular_date))
    res = rangy_obj.value
    assert res == singular_date.toordinal()

@pytest.mark.usefixtures("register_converters")
def test_open_range_rangy():
    start_date = date(2023, 1, 1)
    res = parse_range(Rangy((start_date, "*")))
    assert res[0] == start_date.toordinal()
    assert res[1] is None

@pytest.mark.usefixtures("register_converters")
def test_range_contains_date():
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    range_obj = Rangy((start_date, end_date))
    some_date = date(2023, 6, 15)
    assert some_date.toordinal() in range_obj
    assert date(2024, 1, 1).toordinal() not in range_obj

@pytest.mark.usefixtures("register_converters")
def test_date_converter():
    date_converter = DateConverter()
    some_date = date(2023, 6, 15)
    assert date_converter.to_number(some_date) == some_date.toordinal()
    assert date_converter.to_string(some_date) == some_date.isoformat()