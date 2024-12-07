import pytest
from rangy import Converter, ConverterRegistry

def test_register_and_get_converter():
    ConverterRegistry.clear()
    converter = Converter(int)
    ConverterRegistry.register(converter)
    assert ConverterRegistry.get(int) == converter

def test_get_converter_for_instance():
    ConverterRegistry.clear()
    converter = Converter(int)
    ConverterRegistry.register(converter)
    assert ConverterRegistry.get(1) == converter

def test_get_nonexistent_converter():
    ConverterRegistry.clear()
    with pytest.raises(KeyError):
        ConverterRegistry.get(str)

def test_clear_registry():
    ConverterRegistry.clear()
    converter = Converter(int)
    ConverterRegistry.register(converter)
    ConverterRegistry.clear()
    with pytest.raises(KeyError):
        ConverterRegistry.get(int)

def test_converter_registry_order():
    class CustomType1:
        pass

    class CustomType2:
        pass

    def to_numeric1(obj):
        return 1

    def to_numeric2(obj):
        return 2

    converter1 = Converter(CustomType1, to_numeric1)
    converter2 = Converter(CustomType2, to_numeric2)

    ConverterRegistry.clear()
    ConverterRegistry.register(converter1)
    ConverterRegistry.register(converter2)

    converters = list(ConverterRegistry())
    assert converters[0] == converter1
    assert converters[1] == converter2

if __name__ == "__main__":
    pytest.main()

