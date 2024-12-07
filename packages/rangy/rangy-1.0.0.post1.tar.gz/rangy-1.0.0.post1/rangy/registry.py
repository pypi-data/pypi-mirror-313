from rangy.converters import Converter


class ConverterRegistry:
    """
    A registry for managing `Converter` instances that handle the conversion of custom data types to numeric and string representations.

    The `Rangy` system uses this registry to look up the appropriate `Converter` for a given type. This allows seamless integration of custom data types into the `Rangy` system, which primarily works with numeric ranges.

    Attributes:
        types (dict): A dictionary storing the registered converters, keyed by the type they handle.

    Methods:

        register(converter): Registers a new `Converter` instance.  The converter is stored in the `types` dictionary, keyed by the `_type` attribute of the converter.

        get(_type): Retrieves the registered `Converter` for the given type. Raises a `KeyError` if no converter is registered for that type.  If `_type` is an instance of a class, retrieves by its class instead.

        clear(): Clears all registered converters from the registry, effectively resetting it to an empty state.
        __iter__(): Returns an iterator over the registered `Converter` instances.  Useful for iterating through all available converters.

    Example:

    ```python
    from rangy import Converter, ConverterRegistry, Rangy

    class CustomType:
        def __init__(self, value):
            self.value = value

    def custom_to_numeric(custom_obj):
        return custom_obj.value

    custom_converter = Converter(CustomType, custom_to_numeric)
    ConverterRegistry.register(custom_converter)

    retrieved_converter = ConverterRegistry.get(CustomType)
    assert retrieved_converter == custom_converter

    # or with instance:

    instance = CustomType(5)
    retrieved_converter = ConverterRegistry.get(instance)

    assert retrieved_converter == custom_converter

    for converter in ConverterRegistry():
        print(converter)  # Print all registered converters.
    ```
    """

    types = []

    @classmethod
    def register(cls, converter: Converter):
        """Registers a Converter."""
        cls.types.append(converter)

    @classmethod
    def get(cls, _type):
        """Retrieves a Converter by type."""
        if not isinstance(_type, type):
            _type = _type.__class__
        for converter in cls.types:
            if converter._type == _type:
                return converter
        raise KeyError(f"No converter registered for type {_type}")

    @classmethod
    def clear(cls):
        """Clears all registered converters."""
        cls.types.clear()

    @classmethod
    def __iter__(cls):
        """Returns an iterator over the registered converters."""
        return iter(cls.types)
