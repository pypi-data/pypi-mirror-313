from dataclasses import dataclass
import math
from typing import Optional, Tuple, Union

from rangy import (ANY, ANY_CHAR, AT_LEAST_ONE, EXACT, INFINITY, RANGE, SPECIAL_CHARS)
from rangy.exceptions import ParseRangeError

from .parse import parse_range as new_parse


@dataclass
class RangeBounds:
    min: int
    max: Optional[int]

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
    * **Value access:** Properties `.value` (for exact rangys) and `.values` (for ranges) provide convenient access to rangy information. Raises a ParseRangeError if used inappropriately (e.g., accessing .value when it is representing a range of rangys).
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
        df (RangeBounds): The defnitinition for the range. Note that is neither the human readble nor the internal representation for numbers.
        num (RangeBounds): The definition as numerical (for example ANY == math.inf)
        _rangy_type (int): The type of range.
    """
    def __init__(self, range: Union[int, str, Tuple[int, int]], parse_func: callable = new_parse):
        """
        Initializes a Rangy instance.

        Args:
            rangy (Union[int, str, Tuple[int, int]]): The rangy specification. Can be an integer, string, or tuple representing the rangy.

        Raises:
            ParseRangeError: If the provided `rangy` is in an invalid format.
        """
        self.df = RangeBounds(*parse_func(range))
        self.num = self.to_number()

    def to_number(self):
        mmin, mmax = self.df.min, self.df.max
        if mmax == None:
            mmax =  math.inf
        num = RangeBounds(mmin, mmax)
        return num



    def __lt__(self, other: int) -> bool:
        """
        Checks if the maximum rangy is less than the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the maximum rangy is less than the given value, False otherwise.
        """
        return self.num.max < other

    def __le__(self, other: int) -> bool:
        """
        Checks if the maximum rangy is less than or equal to the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the maximum rangy is less than or equal to the given value, False otherwise.
        """
        return self.num.max <= other

    def __gt__(self, other: int) -> bool:
        """
        Checks if the minimum rangy is greater than the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the minimum rangy is greater than the given value, False otherwise.
        """
        return self.num.min > other

    def __ge__(self, other: int) -> bool:
        """
        Checks if the minimum rangy is greater than or equal to the given value.

        Args:
            other (int): The value to compare against.

        Returns:
            bool: True if the minimum rangy is greater than or equal to the given value, False otherwise.
        """
        return self.num.min >= other

    def __eq__(self, other: Union[int, 'Rangy']) -> bool:
        """
        Checks if the rangy is equal to the given value or another Rangy instance.

        Args:
            other (Union[int, Rangy]): The value or Rangy instance to compare against.

        Returns:
            bool: True if the rangy is equal to the given value or Rangy instance, False otherwise.
        """
        if isinstance(other, Rangy):
            return self.num.min == other.num.min and self.num.max == other.num.max
        return self.num.min == other and self.num.max == other

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
        return self.num.min <= item <= self.num.max

    @property
    def value(self) -> int:
        """
        Returns the exact rangy value.

        Returns:
            int: The exact rangy value.

        Raises:
            ParseRangeError: If the rangy represents a range.
        """
        if self.df.min == self.df.max:
            return self.df.min
        else:
            raise ParseRangeError("Rangy represents a range, use .values instead")

    @property
    def values(self) -> Tuple[int, int]:
        """
        Returns the rangy range as a tuple.

        Returns:
            Tuple[int, int]: The rangy range.

        Raises:
            ParseRangeError: If the rangy represents a single value.
        """
        if self.df.min != self.df.max:
            return (self.df.min, self.df.max)
        else:
            raise ParseRangeError("Rangy represents a single value, use .value instead")

    @property
    def rangy_type(self):
        """
        Returns the type of rangy.

        Returns:
            int: The rangy type.
        """
        return self._type

    def values_to_repr(self):
        def _(value):
            if value == None:
                return ANY_CHAR
            return value
        return _(self.df.min), _(self.df.max)

    def __repr__(self):
        _min, _max = self.values_to_repr()
        if _min == _max:
            return f"Rangy({_min})"
        else:
            return f"Rangy({_min}, {max})"