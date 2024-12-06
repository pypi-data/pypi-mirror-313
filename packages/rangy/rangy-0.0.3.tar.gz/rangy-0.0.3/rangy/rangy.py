from dataclasses import dataclass, field
from typing import Tuple, Union
import re

from rangy import AT_LEAST_ONE, EXACT,ANY, RANGE, INFINITY, ANY_CHAR, ONE_PLUS_CHAR

RangyType = Union[int, str]




def _parse(self, rangy) -> Tuple[Union[int, float], Union[int, float]]:
    """
    Parses a rangy specification into a tuple representing the min and max allowed rangys.

    Args:
        rangy: The rangy specification. Can be one of the following:
            - int: An exact rangy.
            - str: A string representation of an exact rangy or a range.  Ranges can be specified as "min-max", "min+", "+", or "*".  Uses '-', ',', ':', and ';' as separators.
            - tuple: A two-element tuple (min, max) representing the range.  Elements can be int or str.

    Returns:
        A tuple (min_count, max_count) representing the parsed count range.  `INFINITY` is used for open maximums.

    Raises:
        ValueError: If the provided `rangy` is in an invalid format, such as an incorrect range string, a tuple with more than two elements, or non-numeric values.

    Examples:
        - 4  # An integer
        - "4" # A string representing an integer
        - "*"  # Any count
        - "+" # At least one
        - "1-3" # A range
        - (1, 3)  # A tuple range
        - ("1", "3") # A tuple range with strings
        - ("4", "*") # Open-ended range
    """
    range_pattern = re.compile(r"^(\d+|\*|\+)[-,:;](\d+|\*|\+)$")

    if isinstance(rangy, tuple) and len(rangy) == 2:
        min_val, max_val = rangy
        if min_val is None or max_val is None:
            raise ValueError(f"Invalid rangy specification: {rangy}")
    elif isinstance(rangy, str) and range_pattern.match(rangy):
        min_val, max_val = range_pattern.match(rangy).groups()
    elif isinstance(rangy, str) and any(sep in rangy for sep in "-,:;"):
        raise ValueError(f"Invalid rangy specification: {rangy}")
    elif isinstance(rangy, (int, str)):
        min_val = max_val = rangy
    elif rangy == ANY_CHAR:
        min_val = 0
        max_val = INFINITY
    elif rangy == ONE_PLUS_CHAR:
        min_val = 1
        max_val = INFINITY
    else:
        raise ValueError(f"Invalid rangy specification: {rangy}")

    min_val = int(min_val) if min_val not in ("*", "+") else min_val
    max_val = int(max_val) if max_val not in ("*", "+") else max_val

    if min_val == '*':
        min_val = 0
    elif min_val == '+':
        min_val = 1

    if max_val == '*':
        max_val = INFINITY
    elif max_val == '+':
        max_val = INFINITY

    if min_val < 0 or max_val < 0:
        raise ValueError(f"Rangys are always positive, got {min_val}, {max_val}")

    return min_val, max_val


class Rangy:
    """
    Represents a flexible rangy specification, encompassing exact values, ranges, and open rangys.

    This class provides a structured way to define and work with rangys that can be:

    1. **Exact:** A specific integer value (e.g., 4).
    2. **Range:** A range of integers defined by a minimum and maximum value (e.g., 2-4, inclusive). Ranges can be open-ended (e.g., 2+ or + meaning at least 2 or * meaning any number or 2-* meaning 2 or more).
    3. **open:** A rangy representing any non-negative integer (*), or any positive integer (+).

    Internally, a `Rangy` stores the minimum and maximum allowed rangys. For exact rangys, the minimum and maximum are equal. For open rangys, the maximum is represented by a large internal constant (`INFINITY`).

    This class supports:

    * **Construction:** Flexible initialization from integers, strings, or tuples. Various string formats for ranges are supported (e.g., "1-3", "1,3", "1:3", "1;3", "*", "+").
    * **Comparison:** Numerical comparison operators (<, <=, >, >=) against integers, comparing against the maximum allowed rangy of the `Rangy` instance. Equality (==, !=) is supported against both integers and other `Rangy` instances.
    * **Membership testing (`in` operator):** Checks if an integer falls within the defined rangy or range.
    * **Value access:** Properties `.value` (for exact rangys) and `.values` (for ranges) provide convenient access to rangy information. Raises a ValueError if used inappropriately (e.g., accessing .value when it is representing a range of rangys).
    * **Validation:** The `.validate()` method checks if a given integer satisfies the rangy specification.
    * **Rangy Type Determination:** The `._determine_rangy_type()` method allows classification into the four rangy types: rangy_EXACT, rangy_RANGE, rangy_ANY, and rangy_AT_LEAST_ONE.

    **Examples:**

    ```python
    import Rangy
    # Exact rangy
    rangy1 = Rangy(4)  # or Rangy("4")
    assert rangy1.value == 4
    assert rangy1.validate(4)
    assert not rangy1.validate(5)

    # Range rangy
    rangy2 = Rangy("2-4")  # or Rangy((2, 4)) or Rangy(("2", "4"))
    assert rangy2.values == (2, 4)
    assert rangy2.validate(3)
    assert not rangy2.validate(1)

    # open rangy
    rangy3 = Rangy("*")  # Any non-negative integer
    assert rangy3.validate(0)
    assert rangy3.validate(1000)

    rangy4 = Rangy("+")  # Any positive integer
    assert rangy4.validate(1)
    assert not rangy4.validate(0)

    rangy5 = Rangy("1-*")
    assert rangy5.values == (1, 1000000)  # where 1000000 is a large internal constant, INFINITY.
    assert 1 in rangy5
    assert 0 not in rangy5
    assert rangy5._determine_rangy_type() == rangy_RANGE

    rangy6 = Rangy(1)
    assert rangy6._determine_rangy_type() == rangy_EXACT

    rangy7 = Rangy("*")
    assert rangy7._determine_rangy_type() == rangy_ANY

    rangy8 = Rangy("+")
    assert rangy8._determine_rangy_type() == rangy_AT_LEAST_ONE
    ```

    Attributes:
        _min (int): The minimum range value.
        _max (int): The maximum range value.
        _rangy_type (int): The type of range.
    """
    def __init__(self, range: Union[int, str, Tuple[int, int]]):
        """
        Initializes a Rangy instance.

        Args:
            rangy (Union[int, str, Tuple[int, int]]): The rangy specification. Can be an integer, string, or tuple representing the rangy.

        Raises:
            ValueError: If the provided `rangy` is in an invalid format.
        """
        if isinstance(range, Rangy):
            self._min = range._min
            self._max = range._max
            self._type = range._type
        else:
            self._min, self._max = _parse(self, range)
            self._type = self._determine_type()

    def _determine_type(self) -> int:
        """
        Determines the type of rangy.

        Returns:
            int: The rangy type, one of rangy_EXACT, rangy_RANGE, rangy_ANY, or rangy_AT_LEAST_ONE.
        """
        if self._min == 0 and self._max == INFINITY:
            return ANY
        elif self._min == 1 and self._max == INFINITY:
            return AT_LEAST_ONE
        elif self._min == self._max:
            return EXACT
        else:
            return RANGE

    def __lt__(self, other: int) -> bool:
        """
        Checks if the maximum rangy is less than the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the maximum rangy is less than the given value, False otherwise.
        """
        return self._max < other

    def __le__(self, other: int) -> bool:
        """
        Checks if the maximum rangy is less than or equal to the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the maximum rangy is less than or equal to the given value, False otherwise.
        """
        return self._max <= other

    def __gt__(self, other: int) -> bool:
        """
        Checks if the minimum rangy is greater than the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the minimum rangy is greater than the given value, False otherwise.
        """
        return self._min > other

    def __ge__(self, other: int) -> bool:
        """
        Checks if the minimum rangy is greater than or equal to the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the minimum rangy is greater than or equal to the given value, False otherwise.
        """
        return self._min >= other

    def __eq__(self, other: Union[int, 'Rangy']) -> bool:
        """
        Checks if the rangy is equal to the given value or another Rangy instance.

        Args:
            other (Union[int, Rangy]): The value or Rangy instance to compare against.

        Returns:
            bool: True if the rangy is equal to the given value or Rangy instance, False otherwise.
        """
        if isinstance(other, Rangy):
            return self._min == other._min and self._max == other._max
        return self._min == other and self._max == other

    def __ne__(self, other: Union[int, 'Rangy']) -> bool:
        """
        Checks if the rangy is not equal to the given value or another Rangy instance.

        Args:
            other (Union[int, Rangy]): The value or Rangy instance to compare against.

        Returns:
            bool: True if the rangy is not equal to the given value or Rangy instance, False otherwise.
        """
        return not self.__eq__(other)

    def __contains__(self, item: int) -> bool:
        """
        Checks if the given item is within the rangy range.

        Args:
            item (int): The item to check.

        Returns:
            bool: True if the item is within the rangy range, False otherwise.
        """
        return self._min <= item <= self._max

    @property
    def value(self) -> int:
        """
        Returns the exact rangy value.

        Returns:
            int: The exact rangy value.

        Raises:
            ValueError: If the rangy represents a range.
        """
        if self._min == self._max:
            return self._min
        else:
            raise ValueError("Rangy represents a range, use .values instead")

    @property
    def values(self) -> Tuple[int, int]:
        """
        Returns the rangy range as a tuple.

        Returns:
            Tuple[int, int]: The rangy range.

        Raises:
            ValueError: If the rangy represents a single value.
        """
        if self._min != self._max:
            return (self._min, self._max)
        else:
            raise ValueError("Rangy represents a single value, use .value instead")

    def validate(self, rangy: int) -> bool:
        """
        Validates if the given rangy falls within the specified range.

        Args:
            rangy (int): The rangy to validate.

        Returns:
            bool: True if the rangy is within the specified range, False otherwise.
        """
        return self._min <= rangy <= self._max if self._max != float("inf") else rangy >= self._min

    @property
    def rangy_type(self):
        """
        Returns the type of rangy.

        Returns:
            int: The rangy type.
        """
        return self._type

    def __repr__(self):
        if self._min == self._max:
            return f"Rangy({self._min})"
        else:
            return f"Rangy({self._min}, {self._max})"