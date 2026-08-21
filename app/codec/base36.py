"""
Base-36 encoding and decoding utilities for compact integer token serialization.
Standard uppercase alphabet: 0-9, A-Z (radix 36).
"""

BASE36_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE36_MAP = {char: idx for idx, char in enumerate(BASE36_ALPHABET)}


def base36_encode(number: int, min_length: int = 0) -> str:
    """
    Encodes a non-negative integer into a Base-36 uppercase string.
    Optional min_length pads with leading zeros.
    """
    if number < 0:
        raise ValueError(f"Cannot encode negative integer {number} in base36")
    if number == 0:
        encoded = "0"
    else:
        chars = []
        n = number
        while n > 0:
            n, rem = divmod(n, 36)
            chars.append(BASE36_ALPHABET[rem])
        encoded = "".join(reversed(chars))

    if min_length > 0 and len(encoded) < min_length:
        encoded = encoded.zfill(min_length)
    return encoded


def base36_decode(s: str) -> int:
    """
    Decodes a Base-36 string (case-insensitive) into an integer.
    """
    if not s:
        raise ValueError("Cannot decode empty string in base36")
    s_upper = s.upper()
    val = 0
    for char in s_upper:
        if char not in BASE36_MAP:
            raise ValueError(f"Invalid Base-36 character '{char}' in '{s}'")
        val = val * 36 + BASE36_MAP[char]
    return val
