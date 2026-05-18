


def encode_w26_24bit(facility, card):
    if not (0 <= facility <= 255):
        raise ValueError("Facility must be 0–255")
    if not (0 <= card <= 65535):
        raise ValueError("Card must be 0–65535")

    return f"{(facility << 16) | card:X}"

def decode_w26_24bit_hex(hex_str):
    # Parse hex string to integer
    value = int(hex_str, 16)

    if not (0 <= value <= 0xFFFFFF):
        raise ValueError("Must be 24-bit hex value")

    facility = (value >> 16) & 0xFF
    card = value & 0xFFFF

    return facility, card