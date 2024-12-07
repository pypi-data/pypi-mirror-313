.. _ranges:

Ranges
######

The `Rangy` class provides a flexible way to represent counts, including both closed ranges and open-ended ranges.  It also allows specifying an exact count as a special case of a closed range where the minimum and maximum values are the same.

Ranges are a tuple of boundaries: the min and max.  The min and max can be any integer, including negative values.  The min and max are always inclusive. As we'l see bellow, the min and the max can be the, in which case we have a singular range.


The special classes reprent unbounded boundaries:
    **Any** : "*"
    Represent from zero to infinity

    **At least one**: "+"

If a range has one of these two values, it is considered an open range.


Singular  Ranges
****************

Singular ranges do sound like a joke, or they should. What we call singular ranges are ranges that represent a single value.
They only exist to provide a consistent interface with the rest of the library.

In some cases, it's really useful to do stuff on ranges and numbers, and doing so with one interface is really useful.

    Singular ranges are an abstraction that allows you to treat a single value as a range.
    Some key facts about singular ranges:
        - They are always inclusive.
        - Internally, they are represented as a tuple with the same value twice, i.e. min = max.
        - They may be open or closed ranges.

Meaning
=======
If open singular ranges, the meaning is:
* "+" anything greater than one.
* "*" anything greater or equal to one.

Representations:
================
* **Integer representation:** Simply provide an integer.  `Rangy(4)` represents an exact count of 4.

* **String representation:** Provide a string representation of the integer. `Rangy("4")` is equivalent to `Rangy(4)`.

* **Tuple representation:** Provide a tuple with identical integer values. `Rangy((4, 4))` is equivalent to `Rangy(4)`.  Mixed type tuples like `("4", 4)` are also supported.  This form is primarily for consistency, as using the integer or string form directly is generally simpler for exact counts.

Validation
==========
Heres a list of valid and invalid values for a singular range. What we mean if Rangy("x").validates(y) should return:

* `Rangy(4)```:
     * **True**: 4
     * **False** : 3, 5, anything else
*  `Rangy("+")`:
     * **True**: 1,3,4, 3043424324
     * **False**: 0, -1, -30

Closed Ranges
*************

Closed ranges specify a minimum and maximum inclusive count. They can be created using several formats:

Meaning
=======
Closed ranges means a well defined min and max, and for int, a finite number of values.
The values are always inclusive.

Representations:
================

* **String representation:** `"min-max"` where `min` and `max` are integers.  Hyphens, commas, colons, and semicolons can be used interchangeably as separators.  For example, `"2-4"`, `"2,4"`, `"2:4"`, and `"2;4"` are all equivalent and represent a count that must be between 2 and 4 (inclusive).

* **Tuple representation:** `(min, max)` where `min` and `max` are integers. For example, `(2, 4)` also represents a count between 2 and 4 (inclusive). Mixed type tuples like `("2", 4)` are also supported.

Validation
==========
Heres a list of valid and invalid values for a closed ranges. What we mean if Rangy("x").validates(y) should return:

* `Rangy(3, 5)```:
     * **True**: 3, 4, 5
     * **False** : 1,2,6,7, anything else
*  `Rangy("3-4")`:
     * **True**: 3, 4
     * **False**: 1,2,5,6, anything else

Open Ranges
************

Either the min or the max can be open-ended.

Meaning
=======

As the min boundary:

* "+" means more than one up to smaller and equal to the end.
* "*" means any number smaller or equal to the end.

As the max boundary:
* "+" means one more than the min up to infinity.
* "*" means any number greater or equal to the min.

Representations:
================
* **String representation with open maximum:** `"min-*"` or `"min+"` where `min` represents the minimum allowed count. For example, `"2-*"` specifies a count of 2 or more. `"2+"` means is equivalent.  Likewise `"*-3"` is equivalent to "0-3", and `"+-3"` is equivalent to "1-3".

* **Tuple representation with open maximum:**  `(min, "*")` or `(min, "+")` where `min` represents the minimum allowed count. For example `(2, "*")` specifies a count of 2 or more. `(2, "+")` is equivalent. Mixed type tuples like `("2", "*")` are also supported.

Validation
==========
Heres a list of valid and invalid values for a closed ranges. What we mean if Rangy("x").validates(y) should return:
We'll show min any, max any, min at least one, max at least one


* `Rangy("*", 10)`:
     * **True**: 0 through 10.
     * **False** : > 11
*  `Rangy("3-*")`:
     * **True**: 3, 4  anything greater
     * **False**: 1,2
* `Rangy("+", 10)`:
     * **True**: 1 through 10.
     * **False** : 0 and > 11
*  `Rangy("3-+")`:
     * **True**:  4  anything greater
     * **False**: 1,2


Examples
--------

.. code-block:: python

    from rangy import Rangy
    from datetime import date

    # Closed range
    rangy1 = Rangy("2-4")  # or Rangy((2, 4)), Rangy("2,4"), Rangy("2:4"), or Rangy("2;4")

    # Open range (any count)
    rangy2 = Rangy("*")

    # Open range (at least one)
    rangy3 = Rangy("+")

    # Open range (at least 3)
    rangy4 = Rangy("3-*") # or Rangy((3, "*")) or Rangy("3+") or Rangy((3,"+"))

    # Exact count
    rangy5 = Rangy(4) # or Rangy("4") or Rangy((4, 4))

    # Date range
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
    rangy6 = Rangy((start_date, end_date))
    assert rangy6.values == (start_date.toordinal(), end_date.toordinal())

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   range_types


