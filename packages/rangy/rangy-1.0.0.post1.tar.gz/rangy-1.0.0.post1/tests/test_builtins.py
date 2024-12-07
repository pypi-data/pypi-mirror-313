
import pytest

from rangy.converters import Converter


def test_int_converter():
    int_converter = Converter(int)
    assert int_converter.to_number(1) == 1
    assert int_converter.to_number(1.5) == 1.5
    assert int_converter.to_str(1) == "1"
    assert int_converter(1) == 1

def test_float_converter():
    float_converter = Converter(float)
    assert float_converter.to_number(1) == 1.0
    assert float_converter.to_number(1.5) == 1.5
    assert float_converter.to_str(1.0) == "1.0"
    assert float_converter(1) == 1.0