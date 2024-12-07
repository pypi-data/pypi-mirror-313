"""MR Star light device commands."""
from .color import HSColor

# Command parts
COMMAND_PREFIX = 0xBC
COMMAND_SUFFIX = 0x55

# Light commands
COMMAND_SET_POWER = 0x01
COMMAND_SET_COLOR = 0x04
COMMAND_SET_BRIGHTNESS = 0x05

UINT16_MAX = 65535

def _split_uint16(value: int) -> tuple[int, int]:
    if 0 > value or value > UINT16_MAX:
        raise ValueError(f"Value must be between 0 and {UINT16_MAX}, got {value}")
    low_byte = value & 0xFF
    high_byte = (value >> 8) & 0xFF
    return low_byte, high_byte

def format_command(command: int, args: bytes) -> bytes:
    """Formats command with prefix and suffix."""
    if len(args) == 0:
        raise ValueError("Command cannot be empty")
    return bytes([COMMAND_PREFIX, command, len(args), *args, COMMAND_SUFFIX])

def format_power_command(is_on: bool) -> bytes:
    """Formats power command."""
    return format_command(COMMAND_SET_POWER, [(1 if is_on else 0)])

def format_brightness_command(brightness: float) -> bytes:
    """Formats brightness command."""
    if brightness < 0 or brightness > 1:
        raise ValueError("Brightness must be between 0 and 1")
    brightness_value = int(1024 * brightness)
    low_byte, high_byte = _split_uint16(brightness_value)

    return format_command(COMMAND_SET_BRIGHTNESS, [
        high_byte, low_byte, 0x00, 0x00, 0x00, 0x00
    ])

def format_color_command(color: HSColor) -> bytes:
    """Formats color command."""
    hue, sat = color
    hue_low, hue_high = _split_uint16(hue)
    sat_low, sat_high = _split_uint16(int(sat * 10))

    return format_command(COMMAND_SET_COLOR, bytes([
        hue_high, hue_low, sat_high, sat_low, 0x00, 0x00
    ]))
