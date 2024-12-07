# rangy

Rangy is a small but feisty python lib designed to make working with numerical ranges a breeze. It handles both open and closed ranges, provides algorithms for distributing items across ranges, and allows you to treat ranges like numbers in comparisons (e.g., `if x < myrange`).

Full docs at [Rangy Documentation](https://rangy.readthedocs.io/en/latest/index.html).

## Features

* **Expressive Range Definitions:** Define counts as exact values (`4`), ranges (`"2-4"`, `"2-*"`, `"+"`), or unbounded (`"*"`).
* **Intuitive Comparisons:** Compare Rangy objects with integers using standard comparison operators (e.g., `<`, `<=`, `>`, `>=`, `==`, `!=`).
* **Membership Testing:** Check if an integer falls within a Rangy's defined range using the `in` operator.
* **Easy Validation:** Validate if a given count satisfies a Rangy's specification with the `.validate()` method.
* **Clear Value Access:** Use `.value` for exact counts and `.values` for ranges.
* **Intelligent Distribution (via `distribute` function):** Distribute a list of items into sublists according to a set of Rangy specifications, handling both pre-segmented and dynamically divided lists.

## Installation

You can install rangy using pip:

```bash
pip install rangy
```

## Usage

### Defining Rangy Objects

```python
from rangy import Rangy

# Exact count
exact_count = Rangy(4)  # or Rangy("4")

# Range count
range_count = Rangy("2-4")  # or Rangy((2, 4)) or Rangy(("2", "4"))

# Unbounded count (any non-negative integer)
any_count = Rangy("*")

# Unbounded count (at least one)
at_least_one = Rangy("+")

# Open-ended range
open_range = Rangy("2-*") # 2 or more
```

### Comparison and Validation

```python
count = Rangy("1-3")

print(2 in count)  # True
print(4 in count)  # False

print(count.validate(2))  # True
print(count.validate(0))  # False

print(count < 4)  # True (compares against the maximum value of the range)

print(count == 2) # False - the equality against an integer checks if rangy covers only that integer.
print(count == Rangy("1-3")) # True

```

### Distributing Items with distribute

```python
from rangy import Rangy, distribute

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
counts = [Rangy(1), Rangy("2-4"), Rangy("*")]

result = distribute(items, counts)
print(result)  # Output: [[1], [2, 3, 4], [5, 6, 7, 8, 9, 10]]


items_with_separator = [1, 2, "--", 3, 4, 5, 6, "--", 7, 8, 9, 10]
counts_with_separator = [Rangy("1-2"), Rangy("4-6"), Rangy("2-5")]

result_with_separator = distribute(items_with_separator, counts_with_separator)
print(result_with_separator)  # Output: [[1, 2], [3, 4, 5, 6], [7, 8, 9, 10]]


```

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

Tests are done with [pytest](https://github.com/pytest-dev/pytest), makers of happy lives.

### License

[MIT License][def]

[def]: ./LICENSE
