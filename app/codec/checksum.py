"""
XOR Checksum algorithm for the PACT protocol.
Calculates 2-character uppercase hexadecimal XOR checksum over ASCII characters.
"""

def calculate_xor_checksum(text: str) -> str:
    """
    Calculates 2-digit uppercase hex XOR checksum over raw ASCII frame.
    Example:
        calculate_xor_checksum("Q|001|7F3K|15223C03Q0|6QR6VFBQ33") -> "7F"
    """
    val = 0
    for char in text:
        val ^= ord(char)
    return format(val, "02X")


def verify_checksum(full_frame: str) -> bool:
    """
    Verifies the trailing 2-digit checksum in a pipe-delimited frame.
    Returns True if valid, False if invalid or corrupt.
    """
    trimmed = full_frame.strip()
    if "|" not in trimmed:
        return False
    parts = trimmed.rsplit("|", 1)
    if len(parts) != 2:
        return False
    body, expected_crc = parts[0], parts[1].strip()
    computed_crc = calculate_xor_checksum(body)
    return computed_crc.upper() == expected_crc.upper()


def append_checksum(body: str) -> str:
    """
    Computes XOR checksum for body and returns 'body|CRC'.
    """
    crc = calculate_xor_checksum(body)
    return f"{body}|{crc}"
