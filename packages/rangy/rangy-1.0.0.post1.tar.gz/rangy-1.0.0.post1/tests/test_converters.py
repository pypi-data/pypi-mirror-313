import pytest

from rangy import Converter


def test_converter_to_number_with_numeric_function():
    converter = Converter(int, to_numeric=lambda x: x + 1)
    assert converter.to_number(1) == 2

def test_converter_to_number_without_numeric_function():
    converter = Converter(int)
    assert converter.to_number(1) == 1
    assert converter.to_number(1.5) == 1.5

def test_converter_to_number_invalid_value():
    converter = Converter(int)
    with pytest.raises(ValueError):
        converter.to_number("invalid")

def test_converter_to_str_with_string_function():
    converter = Converter(str, to_string=lambda x: f"Value: {x}")
    assert converter.to_str(1) == "Value: 1"

def test_converter_to_str_without_string_function():
    converter = Converter(str)
    assert converter.to_str(1) == "1"

def test_converter_float():
    converter = Converter(float)
    assert converter.__float__(1) == 1.0

def test_converter_int():
    converter = Converter(int)
    assert converter.__int__(1.5) == 1.5

def test_converter_str():
    converter = Converter(str)
    assert converter.__str__(1) == "1"

def test_converter_call():
    converter = Converter(int)
    assert converter(1) == 1