import pytest

from rangy.builtins import DateConverter, register_builtins
from rangy.registry import ConverterRegistry


@pytest.fixture(autouse=True)  # autouse applies to all tests automatically
def register_converters():
    ConverterRegistry.clear()  # Start with a clean registry for each test
    ConverterRegistry.register(DateConverter()) # Register the DateConverter
    register_builtins()