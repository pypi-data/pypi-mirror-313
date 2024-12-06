Rangy: Flexible Count Specifications
====================================

The `rangy` library provides a flexible way to specify and work with count specifications, whether they represent an exact count, a range of counts, or unbounded counts (any count or at least one).

Key Features
------------

* **Flexible Count Representation:**  Supports specifying counts as exact values (e.g., 4), ranges (e.g., "2-4", "1-*"), or unbounded values ("*", "+").
* **Intuitive Parsing:**  Handles various input formats for ranges, including strings ("1-3", "1,3", "1:3"), tuples ((1, 3)), and mixed types (("1", 3)).
* **Comparison Operations:** Enables comparing `Rangy` objects with integers and other `Rangy` objects using standard comparison operators (e.g., <, <=, >, >=, ==, !=).
* **Membership Testing:** Supports using the ``in`` operator to check if a value falls within a specified range.
* **Validation:** Provides a method to validate whether a given count satisfies a `Rangy` specification.
* **Distribution:** Includes a powerful ``distribute()`` function to distribute items into sublists based on `Rangy` specifications, handling both separated and unseparated input lists.  (See : `distribute` for more details).


Basic Usage
-----------

.. code-block:: python

    from rangy import Rangy

    # Exact count
    exact_count = Rangy(4)

    # Range of counts
    range_count = Rangy("2-4")  # or Rangy((2, 4)) or Rangy(("2", "4"))

    # Any count
    any_count = Rangy("*")

    # At least one
    at_least_one_count = Rangy("+")



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ranges
   math
   distribute



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
