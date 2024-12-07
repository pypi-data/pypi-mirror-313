import math
from typing import Any, List

from . import Rangy

SEPERATOR = "--"


def distribute(items: List[Any], rangys: List[Rangy], separator: str = SEPERATOR) -> List[List[Any]]:
    """
    Distributes a list of items into sublists based on flexible count specifications.

    This function intelligently partitions a list of items into multiple sublists according to the provided `Rangy` objects.  It handles both scenarios where the input list is pre-segmented by a separator and cases where it needs to be dynamically divided.

    Args:
        items: The list of items to distribute.
        rangys: A list of `Rangy` objects, each specifying the allowed size range for a corresponding sublist.
        separator: An optional separator string used to pre-segment the `items` list. If present in `items`, the function assumes the list is already divided into groups and distributes accordingly. Defaults to "--".

    Returns:
        A list of sublists, where each sublist's size conforms to the constraints specified by the respective `Rangy` object.

    Raises:
        ValueError: If the number of items cannot be distributed according to the `Rangy` specifications, or if the number of separated groups doesn't match the number of `Rangy` objects.

    Heuristics and Tradeoffs:

    * **Separator Handling:** If a separator is present, the function prioritizes respecting the pre-defined groups in `items`.  This offers greater control over distribution when the input data has inherent segmentation.  The tradeoff is that the `Rangy` constraints must be compatible with the existing group sizes.

    * **Minimum Satisfaction:** The function prioritizes satisfying the minimum count for each `Rangy` first.  This ensures that each sublist receives at least the minimum required number of items.

    * **Proportional Distribution for Unbounded Rangys:** When dealing with unbounded `Rangy` instances (represented by "*" or ranges ending with "*"), the function distributes remaining items proportionally to the minimum values of these unbounded counts. This aims for a balanced distribution when some sublists can accept an arbitrary number of items.  If all minimums of unbounded counts are 0, all remaining items are allocated to the first unbounded range.

    * **Allocation to First Unbounded Range:** If, after proportional distribution to ranges with a minimum greater than 0, there are still items remaining (due to rounding or all minimums being 0), these items are allocated to the *first* unbounded range encountered.

    Known Guesses and Assumptions:

    * **Separator Exclusivity:** The separator is assumed to be used *exclusively* for segmentation. If an item identical to the separator appears within a segment that should not be treated as a separator, unexpected behavior may occur.

    * **Integer Rangys:** The `Rangy` objects are assumed to work with integer counts.  While they internally represent ranges, the final distribution deals with whole numbers of items.

    * **Non-Negative Rangys:**  `Rangy` objects are designed to represent non-negative counts. Negative values will raise a ValueError in count creation.


    Example:

    ```python
    import Rangy, distribute

    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rangys = [Rangy(1),Rangy("2-4"),Rangy("*")]
    result = distribute(items, rangys)
    print(result)  # Output: [[1], [2, 3, 4], [5, 6, 7, 8, 9, 10]]


    items_separated = [1, 2, SEPERATOR, 3, 4, 5, 6, SEPERATOR, 7, 8, 9, 10]
    rangys_separated = [Rangy("1-2"),Rangy("4-6"),Rangy("4-9")]
    result_separated = distribute(items_separated, rangys_separated)
    print(result_separated) # Output: [[1, 2], [3, 4, 5, 6], [7, 8, 9, 10]]



    ```
    """
    if separator in items:
        separated_items = []
        current_group = []
        for item in items:
            if item == separator:
                separated_items.append(current_group)
                current_group = []
            else:
                current_group.append(item)
        separated_items.append(current_group)

        if len(separated_items) != len(rangys):
            raise ValueError("Number of separated groups does not match the number of Rangys.") # pragma: no cover

        # Distribute separated items
        results = []
        for group, c in zip(separated_items, rangys):
            if not len(group) in c:
                raise ValueError(f"Group size does not satisfyRangy {c}.")
            results.append(group)  # Already separated correctly
        return results

    else:  # No separators
        n_items = len(items)
        n_counts = len(rangys)

        # First pass: Determine the number of items for eachRangy
        takes = [0] * n_counts
        remaining_items = n_items

        for i, vc in enumerate(rangys):
            take = vc.num.min  # Ensure minimum is taken
            if vc.num.max != math.inf:  # Bounded Rangys
                take = min(vc.num.max, remaining_items)
            takes[i] = take
            remaining_items -= take

            if remaining_items < sum(vcc.num.min for vcc in rangys[i+1:]):  # Check if there will be enough items to at least meet minimal subsequent rangys
                raise ValueError("Not enough items to distribute")

        # Distribute remaining items to unbounded counts
        infinite_indices = [i for i, vc in enumerate(rangys) if vc.num.max == math.inf]
        if infinite_indices:  # Only distribute if there are any infinite counts
            infinite_count_min_sum = sum(rangys[i].num.min for i in infinite_indices)
            for i in infinite_indices:
                takes[i] += int(remaining_items * (rangys[i].num.min / infinite_count_min_sum) if infinite_count_min_sum > 0 else (1 if i == infinite_indices[0] else 0))  # distribute proportionally, handle division by zero, put all in the first infinite range if all min counts for unbounded counts are 0

            distributed_items = sum(takes)
            if distributed_items != n_items:  # Allocate any remaining to the first infinite range. Should only happen when min counts for unbounded counts are 0
                takes[infinite_indices[0]] += n_items - distributed_items

        # Second pass: Distribute items based on calculated takes
        result = [[] for _ in rangys]
        item_index = 0

        for i, take in enumerate(takes):
            result[i].extend(items[item_index:int(item_index + take)])
            item_index += int(take)
        # Validate AND check if we've ignored some arguments.
        if item_index != len(items):
            raise ValueError(f"Too many arguments provided. {len(items) - item_index} extra argument(s) found.") # pragma: no cover

        # Validation
        for i, vc in enumerate(rangys):
            if not len(result[i]) in vc:
                raise ValueError(f"Group {i + 1} size does not satisfyRangy {vc}.")

        return result

