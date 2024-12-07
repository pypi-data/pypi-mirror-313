from datetime import date

class Converter():
    """
    Facilitates conversion of custom data types to numeric and string representations for use within the `Rangy` system.

    The `Rangy` system works primarily with numeric ranges.  This `Converter` class allows you to seamlessly integrate custom data types that might not inherently have numeric or string representations suitable for range comparisons.  It bridges the gap by providing conversion logic to and from numeric and string forms.

    Args:
        _type (type): The custom data type that this converter handles.  This is used for type lookup in the `ConverterRegistry`.
        to_numeric (callable, optional): A function that takes an instance of your custom type and returns a numeric value (int or float). If not provided, the converter attempts to cast the value to float, then int. Defaults to None.
        to_string (callable, optional): A function that takes an instance of your custom type and returns its string representation. If not provided, the built-in `str()` is used. Defaults to None.


    Methods:

        to_number(value): Converts a value of the custom type to a numeric representation.  Uses the `to_numeric` function if provided, otherwise attempts direct casting.

        to_str(value): Converts a value of the custom type to a string representation. Uses the `to_string` function if provided, otherwise uses the built-in `str()`.

        __call__(value):  Makes instances of the `Converter` callable.  Equivalent to calling `to_number(value)`.  This allows convenient use within other parts of the `Rangy` system.

        __float__(value):  Similar to `to_number`, but specifically attempts to return a float representation. Primarily used internally.

        __int__(value): Similar to `to_number`, but specifically attempts to return an integer representation. Primarily used internally.
        __str__(value): Synonymous with `to_str(value)`. Used for string conversions, mainly internally.


    Example:

    ```python
    from rangy import Converter, ConverterRegistry, Rangy, parse_range

    class CustomType:
        def __init__(self, value):
            self.value = value

    # Define conversion functions
    def custom_to_numeric(custom_obj):
        return custom_obj.value

    def custom_to_string(custom_obj):
        return f"CustomValue({custom_obj.value})"


    # Create and register the converter
    custom_converter = Converter(CustomType, custom_to_numeric, custom_to_string)
    ConverterRegistry.register(custom_converter)

    # Now you can use CustomType in ranges:
    range_tuple = parse_range(("1", CustomType(5)))
    print(range_tuple)    # output: (1, 5)

    range_tuple = parse_range((CustomType(2), "4"))
    print(range_tuple) # output (2, 4)


    rangy_obj = Rangy((CustomType(1), CustomType(3)))
    print(2 in rangy_obj) # output: True
    ```


    Raises:
        ValueError: If the input value cannot be converted to a number (when `to_numeric` fails or direct casting is unsuccessful).

    """

    def __init__(self, _type, to_numeric=None, to_string=None):
        self._type = _type
        self.to_numeric = to_numeric
        self.to_string = to_string

    def to_number(self, value):

        if self.to_numeric:
            return self.to_numeric(value)
        try:
            return float(value)
        except ValueError:
            try:
                return int(value)
            except ValueError:
                raise ValueError("Could not convert value to number")

    def to_str(self, value):
        if self.to_string:
            return self.to_string(value)
        return str(value)

    def __float__(self, value): # pragma: no cover
        return self.to_number(value)

    def __int__(self, value):# pragma: no cover
        return self.to_number(value)

    def __str__(self, value): # pragma: no cover
        return self.to_str(value)

    def __call__(self, value): # pragma: no cover
        return self.to_number(value)

