.. _ranges:

Ranges
======

The `Rangy` class provides a flexible way to represent counts, including both closed ranges and open-ended ranges.  It also allows specifying an exact count as a special case of a closed range where the minimum and maximum values are the same.


Closed Ranges
-------------

Closed ranges specify a minimum and maximum inclusive count. They can be created using several formats:

* **String representation:** `"min-max"` where `min` and `max` are integers.  Hyphens, commas, colons, and semicolons can be used interchangeably as separators.  For example, `"2-4"`, `"2,4"`, `"2:4"`, and `"2;4"` are all equivalent and represent a count that must be between 2 and 4 (inclusive).

* **Tuple representation:** `(min, max)` where `min` and `max` are integers. For example, `(2, 4)` also represents a count between 2 and 4 (inclusive). Mixed type tuples like `("2", 4)` are also supported.


Open Ranges
-----------

Open ranges allow for unbounded maximums. These are represented using the following formats:

* **`*`**: Represents *any* count (0 or greater). Equivalent to "0-\*".

* **`+`**: Represents a count of at least one (1 or greater). Equivalent to "1-\*".

* **String representation with open maximum:** `"min-*"` or `"min+"` where `min` represents the minimum allowed count. For example, `"2-*"` specifies a count of 2 or more. `"2+"` is equivalent.  Likewise `"*-3"` is equivalent to "0-3", and `"+-3"` is equivalent to "1-3".

* **Tuple representation with open maximum:**  `(min, "*")` or `(min, "+")` where `min` represents the minimum allowed count. For example `(2, "*")` specifies a count of 2 or more. `(2, "+")` is equivalent. Mixed type tuples like `("2", "*")` are also supported.



Exact Counts (Identity Ranges)
------------------------------

You can use `Rangy` to represent an exact count by specifying a closed range where the minimum and maximum values are the same.

* **Integer representation:** Simply provide an integer.  `Rangy(4)` represents an exact count of 4.

* **String representation:** Provide a string representation of the integer. `Rangy("4")` is equivalent to `Rangy(4)`.

* **Tuple representation:** Provide a tuple with identical integer values. `Rangy((4, 4))` is equivalent to `Rangy(4)`.  Mixed type tuples like `("4", 4)` are also supported.  This form is primarily for consistency, as using the integer or string form directly is generally simpler for exact counts.


Examples
--------

.. code-block:: python

    from rangy import Rangy

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


