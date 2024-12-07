import re

from rangy.exceptions import ParseRangeError

from .const import INFINITY, SPECIAL_CHARS
from .registry import ConverterRegistry


def _split(as_squence):
    """
    Splits a sequence into a tuple of two values.
    It will ensure only sequences of length 1 or 2 are accepted and
    that no None values are present.

    Args:
        as_squence: The sequence to split, str, list, tuple.
    Raises:
        ParseRangeError: If the input is invalid.
    Returns:
        A tuple of two values.
    """
    if None ==  as_squence:
        raise ParseRangeError("Invalid range tuple/list")
    if len(as_squence) == 1:
        # this is valid, as it
        # indicates a single value range
        return as_squence[0], as_squence[0]
    elif len(as_squence) == 2:
        return as_squence[0], as_squence[1]
    else:
        raise ParseRangeError("Invalid range tuple/list length")

def _nomalize_str(range_str):
    """
    Normalizes a range string by removing brackets and splitting it into parts.

    "1-5" -> ["1", "5"]
    "(1-5)" -> ["1", "5"]
    "1-5" -> ["1", "5"]
    "(1,3)"

    Args:
        range_str: The range string to normalize.
    Returns:
        A tuples of parts of the range string.
    """
    range_str = re.sub(r'^[\[\(]|[\]\)]$', '', range_str.strip())  # Remove brackets
    range_str = re.split(r'[\s,;:|-]+', range_str) # split
    return tuple(part.strip() for part in range_str if part.strip()) # Remove empty strings

def _normalize_to_sequence(range_input):
    """Normalizes various range inputs into a consistent tuple representation.

    Args:
        range_input: The range input, which can be a string, tuple, int, etc.

    Returns:
        A tuple (start, end) representing the normalized range.

    Raises:
        ParseRangeError: If the input is invalid or cannot be normalized.
    """
    from rangy import Rangy
    if isinstance(range_input, Rangy):
        range_input = range_input.copy().values

    if isinstance(range_input, (tuple, list)):
        return _split(range_input)
    elif isinstance(range_input, int):
        return range_input, range_input  #

    elif isinstance(range_input, str):
        return _split(_nomalize_str(range_input))
    else:
        raise ParseRangeError(f"Unsupported range input type: {type(range_input)}")


def _normalize_open_char(part, is_min):
    if part in SPECIAL_CHARS.values():
        if is_min:
            if part == "*":
                return 0
            elif part == "+":
                return 1
        else:
            if part == "*":
                return None
            elif part == "+":
                return None
        return part
    return False

def _convert_part(part, is_min):
    for converter in ConverterRegistry():
        try:
            return converter(part)
        except (ValueError, TypeError):
            pass  # Try the next converter
    raise ParseRangeError(f"Unsupported range part: {part}")

def parse_part(part, is_min):
    normalized = _normalize_open_char(part, is_min)
    if normalized is not False:
        return  normalized
    return _convert_part(part, is_min)


def parse_range(range_input):
    """
    Parses a range into a tuple of converted (start, end) values.
    It returns a suitable tuple that is a Range object, that is a tuple of two
    ints, where the second value can be None.

    It normalizes open range tokens and converts other tokens using the
    registered converters.

    Open-ended tokens are transformed into:
        - The min part: 0 for "*", 1 for "+",
        - The max part: None for "*", "+"
    Examples:

    - singulars:
        - "4"  # (4, 4)
        - 4 # (4, 4)
        - (4) # (4, 4)
    - closed ranges:
        - "2,3" # (2, 3)
        - "2-3" # (2, 3)
        - (2, 3) # (2, 3)
    - open range:
        - "*" # (0, None)
        - "+" # (1, None)
        - "*-10" # (0, 10)
        - "+-10" # (1, 10)
        - "10-*" # (10, None)


    Args:
        range_input: The range input (string, tuple, int, etc.)

    Returns:
        A tuple of ints (start, end) with converted values. None represents open-ended ranges.

    Raises:
        ParseRangeError: If the input is invalid or cannot be parsed.
    """
    from rangy import Rangy
    # short circuit if it's already a rangy
    if isinstance(range_input, Rangy):
        return range_input.values

    start, end = _normalize_to_sequence(range_input)

    try:
        _min, _max = parse_part(start, True), parse_part(end, False)
        return parse_part(start, is_min=True), parse_part(end, is_min=False)

    except (KeyError, ValueError, TypeError) as e:
        raise ParseRangeError(f"Error parsing range: {e}") from e
