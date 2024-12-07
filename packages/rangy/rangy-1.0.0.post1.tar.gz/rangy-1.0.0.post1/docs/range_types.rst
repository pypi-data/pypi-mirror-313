
Range Types
===========

The `Rangy` library supports various types of ranges, including integer ranges and date ranges. Additionally, you can add new types by creating custom converters.

Integer Ranges
--------------

Integer ranges are the most basic type of range supported by `Rangy`. They can represent exact counts, closed ranges, and open ranges.

.. code-block:: python

    from rangy import Rangy

    # Exact count
    exact_count = Rangy(4)

    # Closed range
    closed_range = Rangy("2-4")

    # Open range (any count)
    open_range_any = Rangy("*")

    # Open range (at least one)
    open_range_at_least_one = Rangy("+")

Date Ranges
-----------

Date ranges allow you to work with ranges of dates. The `DateConverter` is used to convert dates to their ordinal representation.

.. code-block:: python

    from rangy import Rangy
    from datetime import date

    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    date_range = Rangy((start_date, end_date))

    assert date_range.values == (start_date.toordinal(), end_date.toordinal())

Adding New Types
----------------

You can add support for new types by creating custom converters. A converter defines how to convert a custom type to a numeric and string representation.

.. code-block:: python

    from rangy import Converter, ConverterRegistry, Rangy

    class CustomType:
        def __init__(self, value):
            self.value = value

    def custom_to_numeric(custom_obj):
        return custom_obj.value

    def custom_to_string(custom_obj):
        return f"CustomValue({custom_obj.value})"

    custom_converter = Converter(CustomType, custom_to_numeric, custom_to_string)
    ConverterRegistry.register(custom_converter)

    custom_range = Rangy((CustomType(1), CustomType(3)))
    assert 2 in custom_range