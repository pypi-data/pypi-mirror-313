.. module:: rangy

Distribute
==========

The ``distribute`` function provides a flexible mechanism for distributing a list of items into sublists according to a set of :class:`Rangy` count specifications. This is particularly useful when dealing with data segmentation tasks where the number of elements in each segment can vary within defined constraints.

Basic Usage
-----------

The simplest use case involves distributing items according to a list of :class:`Rangy` objects representing the desired counts for each sublist:

.. code-block:: python

    from rangy import Rangy, distribute

    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    counts = [Rangy(1), Rangy("2-4"), Rangy("*")]  # 1 item, 2-4 items, the rest

    result = distribute(items, counts)
    print(result)  # Output: [[1], [2, 3, 4], [5, 6, 7, 8, 9, 10]]


Handling Separators
-------------------

In scenarios where the input list contains separators that delimit logical segments, ``distribute`` can intelligently handle these boundaries.  The function ensures that separators are not included in the distributed sublists and that segment boundaries are respected.

.. code-block:: python

    items_with_separator = [1, 2, "--", 3, 4, 5, 6, "--", 7, 8, 9, 10]
    counts_with_separator = [Rangy("1-2"), Rangy("4-6"), Rangy("2-5")]

    result_with_separator = distribute(items_with_separator, counts_with_separator)
    print(result_with_separator)  # Output: [[1, 2], [3, 4, 5, 6], [7, 8, 9, 10]]


Unbounded Counts
----------------

``distribute`` supports unbounded counts using the ``*`` and ``+`` specifications within the :class:`Rangy` objects.  ``*`` represents "zero or more," while ``+`` represents "one or more."  When an unbounded count is encountered, ``distribute`` allocates the remaining items to that sublist after satisfying the constraints of the other specified counts.


.. code-block:: python

    items = [1, 2, 3, 4, 5, 6]
    counts = [Rangy(1), Rangy("*")]  # One item, then the rest.

    result = distribute(items, counts)
    print(result)  # Output: [[1], [2, 3, 4, 5, 6]]

Multiple Unbounded Counts
-------------------------

If multiple unbounded counts are specified, ``distribute`` distributes the remaining items among them proportionally.  This ensures that no single unbounded count consumes all the remaining items unless it is the only unbounded count.

.. code-block:: python

    items = [1, 2, 3, 4, 5, 6, 7, 8]
    counts = [Rangy(1), Rangy("*"), Rangy("*")] # One item, then split the rest

    result = distribute(items, counts)
    print(result)  # Output: [[1], [2, 3, 4], [5, 6, 7, 8]] (approximately even split)


Edge Cases and Behavior
-----------------------

* **Insufficient Items:** If there are fewer items than required by the minimum specified counts, ``distribute`` will raise a :exc:`ValueError`.

* **Empty Counts List:**  If an empty list of counts is provided, ``distribute`` will return an empty list of sublists.

* **Separator Handling with Non-String Separators:** If your separator is not a string type, you will need to provide a ``separator_type`` for it to be correctly excluded from the output sublists.

.. code-block:: python

    items_with_int_separator = [1, 2, 3, 4, 5]
    counts = [Rangy(2), Rangy(1)]  # Expect: [[1, 2], [4]]
    separator = 3
    separator_type = int
    result = distribute(items_with_int_separator, counts, separator=separator, separator_type=separator_type)



