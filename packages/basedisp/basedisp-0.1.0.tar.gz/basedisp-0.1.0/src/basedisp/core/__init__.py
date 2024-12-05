"""Core Base Conversion Functionality"""

__all__ = ["from_decimal", "to_decimal", "conversion"]


def from_decimal(number: int, base: int) -> list[int]:
    """Convert a decimal number to a different base.

    Parameters
    ----------
    number : int
        The decimal number to convert
    base : int
        The base to convert to

    Returns
    -------
    list[int]
        List of digits in the target base, ordered from most to least significant

    Examples
    --------
    >>> from_decimal(42, 2)
    [1, 0, 1, 0, 1, 0]  # represents binary 101010
    >>> from_decimal(15, 16)
    [15]  # represents hex F
    """
    if number == 0:
        return [0]

    out: list[int] = []
    while number != 0:
        out.append(number % base)
        number = number // base
    out = out[::-1]
    return out


def to_decimal(number: list[int], base: int) -> int:
    """Convert a number from a given base to decimal.

    Parameters
    ----------
    number : list[int]
        List of digits in the source base, ordered from most to least significant
    base : int
        The base of the input number

    Returns
    -------
    int
        The decimal (base-10) representation

    Raises
    ------
    TypeError
        If the input number is not a list of integers

    Examples
    --------
    >>> to_decimal([1, 0, 1, 0, 1, 0], 2)
    42  # converts binary 101010 to decimal
    >>> to_decimal([15], 16)
    15  # converts hex F to decimal
    """
    try:
        assert isinstance(number, list)
        assert isinstance(number[0], int)
    except AssertionError:
        raise TypeError("Invalid number being converted from base %d", base)

    out: int = sum([orig * (base**power) for power, orig in enumerate(number)])
    return out


def conversion(
    number: list[int] | int, base_initial: int, base_final: int
) -> int | list[int]:
    """Convert a number between any two bases.

    Parameters
    ----------
    number : list[int] | int
        If base_initial is 10, this should be an integer.
        Otherwise, it should be a list of digits in the initial base
    base_initial : int
        The base of the input number
    base_final : int
        The desired output base

    Returns
    -------
    int | list[int]
        If base_final is 10, returns an integer.
        Otherwise, returns a list of digits in the final base

    Examples
    --------
    >>> conversion([1, 0, 1, 0], 2, 10)  # binary to decimal
    10
    >>> conversion(10, 10, 2)  # decimal to binary
    [1, 0, 1, 0]
    """
    if base_initial == 10 and isinstance(number, int):
        return from_decimal(number, base_final)
    assert not isinstance(number, int)
    if base_final == 10:
        return to_decimal(number, base_initial)
    return from_decimal(to_decimal(number, base_initial), base_final)
