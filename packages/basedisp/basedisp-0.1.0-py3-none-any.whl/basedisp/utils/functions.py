"""Utility functions for basecon"""


def left_pad(vals: list[str], total_length: int) -> list[str]:
    """Pad a list of strings with leading zeros to reach a specified length.

    Parameters
    ----------
    vals : list[str]
        List of strings to pad
    total_length : int
        Desired total length after padding

    Returns
    -------
    list[str]
        Padded list of strings

    Examples
    --------
    >>> left_pad(['1', '2', '3'], 5)
    ['0', '0', '1', '2', '3']
    """
    num_needed = max(0, total_length - len(vals))
    prepend = ["0"] * num_needed
    out = prepend + vals
    return out


def make_integer(number: str) -> int:
    """Convert a string to an integer, ensuring no information is lost.

    Parameters
    ----------
    number : str
        String representation of a number

    Returns
    -------
    int
        Integer value

    Raises
    ------
    TypeError
        If the string cannot be unambiguously converted to an integer

    Examples
    --------
    >>> make_integer("42")
    42
    >>> make_integer("3.14")  # raises TypeError
    """
    try:
        number_float = float(number)
        number_int = int(number)
        assert float(number_int) == number_float
    except (ValueError, AssertionError):
        raise TypeError(
            f"number ({number}) cannot be unambiguously converted to an integer"
        )
    return number_int


def clean_inputs(numbers: str | list[str]) -> list[int]:
    """Convert string input(s) to a list of integers.

    Parameters
    ----------
    numbers : str | list[str]
        Space-separated string of numbers or list of number strings

    Returns
    -------
    list[int]
        List of integers

    Examples
    --------
    >>> clean_inputs("1 2 3")
    [1, 2, 3]
    >>> clean_inputs(["42", "255"])
    [42, 255]
    """
    if isinstance(numbers, str):
        numbers = numbers.split(sep=" ")
    out = [make_integer(number) for number in numbers]
    return out


def lowest_multiple(multiple: int, number: int) -> int:
    """Find the lowest multiple of a number that is greater than or equal to another number.

    Parameters
    ----------
    multiple : int
        The base multiple
    number : int
        The number to find the next multiple for

    Returns
    -------
    int
        Lowest multiple of 'multiple' that is >= 'number'

    Examples
    --------
    >>> lowest_multiple(8, 12)
    16
    >>> lowest_multiple(5, 15)
    15
    """
    if not number % multiple:
        return number
    else:
        return multiple * (number // multiple + 1)
