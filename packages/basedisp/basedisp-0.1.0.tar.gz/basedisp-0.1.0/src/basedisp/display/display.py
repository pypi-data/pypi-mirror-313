from ..core import from_decimal
from .bases import BASE16, BASE64, ASCII
from ..utils.functions import left_pad, lowest_multiple

# !todo: Add base64 display


def display_hex(number: int, num_digits=0) -> str:
    """Convert a decimal number to hexadecimal display format.

    Parameters
    ----------
    number : int
        Decimal number to convert
    num_digits : int, optional
        Minimum number of digits to display (will pad with leading zeros)

    Returns
    -------
    str
        Hexadecimal representation prefixed with 'x'

    Examples
    --------
    >>> display_hex(255, 4)
    'x00FF'
    >>> display_hex(15)
    'xF'
    """
    return "x" + "".join(
        left_pad([BASE16[i] for i in from_decimal(number, base=16)], num_digits)
    )


def display_binary(number: int, num_digits=0) -> str:
    """Convert a decimal number to binary display format.

    Parameters
    ----------
    number : int
        Decimal number to convert
    num_digits : int, optional
        Minimum number of digits to display (will pad with leading zeros)

    Returns
    -------
    str
        Binary representation prefixed with 'b'

    Examples
    --------
    >>> display_binary(5, 8)
    'b00000101'
    >>> display_binary(3)
    'b11'
    """
    return "b" + "".join(
        left_pad([str(i) for i in from_decimal(number, base=2)], num_digits)
    )


def display_base64(number: int, num_digits: int = 0) -> str:
    return "o" + "".join(
        left_pad([BASE64[i] for i in from_decimal(number, base=64)], num_digits)
    )


def display_ascii(number: int) -> str:
    """Convert a decimal number to its ASCII representation.

    Parameters
    ----------
    number : int
        Decimal number to convert

    Returns
    -------
    str
        ASCII representation or 'NOT ASCII' if number is out of range

    Examples
    --------
    >>> display_ascci(65)
    'A            '
    >>> display_ascci(7)
    '[BEL]  (\\a)   '
    """
    try:
        out = ASCII[number]
    except KeyError:
        out = "NOT ASCII    "
    return out


def get_lengths(numbers: list[int]) -> tuple[int, int, int, int]:
    """Calculate display lengths needed for decimal, binary, hex, and base64 representations.

    Parameters
    ----------
    numbers : list[int]
        List of numbers to calculate display lengths for

    Returns
    -------
    tuple[int, int, int, int]
        Tuple of (decimal_length, binary_length, hex_length, base64_length) where:
        - decimal_length is the width needed for the largest decimal representation
        - binary_length is the width needed for binary, padded to multiple of 8 bits
        - hex_length is the width needed for hex, padded to multiple of 2 digits
        - base64_length is the width needed for the largest base64 representation

    Examples
    --------
    >>> get_lengths([63, 64, 65])
    (2, 8, 2, 2)  # 2 decimal digits (65)
                  # 8 binary digits (01000001)
                  # 2 hex digits (41)
                  # 2 base64 digits (11)
    >>> get_lengths([255, 256])
    (3, 8, 2, 2)  # 3 decimal digits (256)
                  # 8 binary digits (100000000)
                  # 2 hex digits (FF)
                  # 2 base64 digits (40)
    """
    max_num = max(numbers)
    len_dec = len(str(max_num))
    len_bin = lowest_multiple(8, len(bin(max_num)[2:]))  # Strip '0b' prefix
    len_hex = lowest_multiple(2, len(hex(max_num)[2:]))  # Strip '0x' prefix
    len_base64 = len(from_decimal(max_num, 64))
    return len_dec, len_bin, len_hex, len_base64


def display_single(number: int, len_dec: int, len_bin: int, len_hex: int, len_base64: int) -> str:
    """Format a single number for display in decimal, binary, hex, base64, and ASCII.

    Parameters
    ----------
    number : int
        Number to display
    len_dec : int
        Width for decimal representation
    len_bin : int
        Width for binary representation (excluding 'b' prefix)
    len_hex : int
        Width for hexadecimal representation (excluding 'x' prefix)
    len_base64 : int
        Width for base64 representation

    Returns
    -------
    str
        Formatted string with all representations aligned in columns

    Examples
    --------
    >>> display_single(65, 3, 8, 2, 2)
    ' 65  b01000001  x41  11  A            '
    >>> display_single(63, 3, 8, 2, 2)
    ' 63  b00111111  x3F  0/  ?            '
    >>> display_single(7, 3, 8, 2, 2)
    '  7  b00000111  x07  07  [BEL]  (\\a)   '
    """
    return (
        f"{"".join(left_pad(list(str(number)), len_dec))}  "
        f"{display_binary(number, len_bin)}  "
        f"{display_hex(number, len_hex)}  "
        f"{display_base64(number, len_base64)}  "
        f"{display_ascii(number)}"
    )


def display_multiple(numbers: list[int]) -> str:
    """Format multiple numbers for display, aligned in columns.

    Parameters
    ----------
    numbers : list[int]
        List of numbers to display

    Returns
    -------
    str
        Multi-line string with all numbers formatted in aligned columns showing
        decimal, binary, hexadecimal, base64, and ASCII representations

    Examples
    --------
    >>> print(display_multiple([63, 64, 65]))
    63  b00111111  x3F  0/  ?
    64  b01000000  x40  10  @
    65  b01000001  x41  11  A

    >>> print(display_multiple([7, 8, 9]))
    7  b00000111  x07  07  [BEL]  (\\a)
    8  b00001000  x08  08  [BS]   (\\b)
    9  b00001001  x09  09  [HT]   (\\t)

    >>> print(display_multiple([255, 256]))
    255  b11111111  xFF  3/  NOT ASCII
    256  b100000000 x100 40  NOT ASCII
    """
    max_vals = get_lengths(numbers)
    out = "\n".join([display_single(number, *max_vals) for number in numbers])
    return out
