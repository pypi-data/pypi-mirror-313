.. _math-operators:

Mathematical Operators
======================

The `Rangy` class supports comparison operators to check how a `Rangy` instance relates to a given integer.  These comparisons are performed against the *maximum* allowed value for the `Rangy` instance when using `<` or `<=`, and against the *minimum* allowed value when using `>` or `>=`.


Less Than (<)
----------------

Checks if the *maximum* value of the `Rangy` instance is strictly less than a given integer.

.. code-block:: python

    from rangy import Rangy

    rangy = Rangy("1-3")  # Maximum is 3
    assert rangy < 4  # True
    assert rangy < 3  # False


Less Than or Equal To (<=)
--------------------------

Checks if the *maximum* value of the `Rangy` instance is less than or equal to a given integer.


.. code-block:: python

    from rangy import Rangy

    rangy = Rangy("1-3")  # Maximum is 3
    assert rangy <= 3  # True
    assert rangy <= 4  # True
    assert rangy <= 2  # False


Greater Than (>)
----------------

Checks if the *minimum* value of the `Rangy` instance is strictly greater than a given integer.

.. code-block:: python

    from rangy import Rangy

    rangy = Rangy("1-3")  # Minimum is 1
    assert rangy > 0  # True
    assert rangy > 1  # False



Greater Than or Equal To (>=)
------------------------------

Checks if the *minimum* value of the `Rangy` instance is greater than or equal to a given integer.


.. code-block:: python

    from rangy import Rangy

    rangy = Rangy("1-3")  # Minimum is 1
    assert rangy >= 1  # True
    assert rangy >= 0  # True
    assert rangy >= 2  # False



Equality (==) and Inequality (!=)
----------------------------------

Equality and inequality can be checked against both integers and other `Rangy` instances.  When comparing against an integer, the `Rangy` instance is considered equal if the integer falls *within* the allowed range. When comparing against another `Rangy` instance, both the minimum and maximum values must match.

.. code-block:: python

    from rangy import Rangy

    rangy1 = Rangy("1-3")
    rangy2 = Rangy(2)
    rangy3 = Rangy("1-3")

    assert rangy1 == 2  # True (2 is within the range 1-3)
    assert rangy1 == rangy3 # True (both represent the range 1-3)
    assert rangy1 != 0  # True (0 is not within the range 1-3)
    assert rangy1 != rangy2 # True (ranges are different)

Membership testing using the `in` operator.

The `in` operator can be used to test if an integer falls within the `Rangy` object's specified range.

.. code-block:: python

    from rangy import Rangy

    rangy = Rangy("1-3")

    assert 1 in rangy  # True
    assert 2 in rangy  # True
    assert 3 in rangy  # True
    assert 0 in rangy  # False
    assert 4 in rangy  # False
