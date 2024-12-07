# standard libraries:
from struct import unpack
from tkinter import Misc
from re import fullmatch

# third-party libraries:
from numpy import ndarray, linspace


class Color:
    DEFAULT_LUMINANCE_THRESHOLD: float = 128.
    MINIMUM_PALLETE_SIZE: int = 2

    LUMINANCE_RED_COEFFICIENT: float = .2126
    LUMINANCE_GREEN_COEFFICIENT: float = .7152
    LUMINANCE_BLUE_COEFFICIENT: float = .0722

    def __init__(self):
        raise TypeError("This class is not intended to be instantiated.")

    @staticmethod
    def generate_palette(start_hex: str, end_hex: str, num_colors: int = MINIMUM_PALLETE_SIZE) -> list[str]:
        if num_colors < Color.MINIMUM_PALLETE_SIZE:
            error_message: str = "Number of colors must be at least {}.".format(Color.MINIMUM_PALLETE_SIZE)
            raise ValueError(error_message)
        start_color: tuple[int, int, int] = Color.hex_to_rgb(start_hex)
        end_color: tuple[int, int, int] = Color.hex_to_rgb(end_hex)
        colors: list[str] = []
        for index in range(num_colors):
            rgb_values: ndarray = linspace(start=start_color, stop=end_color, num=num_colors, dtype=int)[index]
            hex_color_code: str = Color.rgb_to_hex(*rgb_values)
            colors.append(hex_color_code)
        return colors

    @staticmethod
    def adjust_brightness(hex_code: str, factor: float = 1.) -> str:
        def clamp(value: int) -> int:
            value = max(10, value)
            scaled_value: int = int(value * factor)
            clamped_value: int = max(0, scaled_value)
            return min(255, clamped_value)
        rgb_values: tuple[int, int, int] = Color.hex_to_rgb(hex_code)
        red_adjusted, green_adjusted, blue_adjusted = map(clamp, rgb_values)
        if factor > 1.0:
            red_adjusted = max(red_adjusted, 1)
            green_adjusted = max(green_adjusted, 1)
            blue_adjusted = max(blue_adjusted, 1)
        return Color.rgb_to_hex(red_adjusted, green_adjusted, blue_adjusted)

    @staticmethod
    def grant_hex_code(master: Misc, hex_code: str) -> str:
        if Color.is_hex_code(hex_code):
            return hex_code
        rgb_values: tuple[int, int, int] = master.winfo_rgb(color=hex_code)
        hex_code = Color.rgb_to_hex(*rgb_values)
        return hex_code

    @staticmethod
    def luminance(red_value: int, green_value: int, blue_value: int) -> float:
        return Color.LUMINANCE_RED_COEFFICIENT * red_value + Color.LUMINANCE_GREEN_COEFFICIENT * green_value + Color.LUMINANCE_BLUE_COEFFICIENT * blue_value

    @staticmethod
    def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
        if not Color.is_hex_code(hex_code):
            error_message: str = "Invalid hex code format: {}".format(hex_code)
            raise ValueError(error_message)
        normalized_hex_code: str = hex_code.lstrip("#")
        if len(normalized_hex_code) == 3:
            normalized_hex_code = "".join(character * 2 for character in normalized_hex_code)
        hex_color_bytes: bytes = bytes.fromhex(normalized_hex_code)
        return unpack("BBB", hex_color_bytes)

    @staticmethod
    def rgb_to_hex(red_value: int, green_value: int, blue_value: int) -> str:
        def clamp(value: int) -> int:
            clamped_value: int = max(0, value)
            return min(255, clamped_value)
        rgb_values: tuple[int, int, int] = red_value, green_value, blue_value
        red_adjusted, green_adjusted, blue_adjusted = map(clamp, rgb_values)
        if not all(0 <= value <= 255 for value in (red_adjusted, green_adjusted, blue_adjusted)):
            raise ValueError("RGB values must be between 0 and 255.")
        return "#{:02X}{:02X}{:02X}".format(red_adjusted, green_adjusted, blue_adjusted)

    @staticmethod
    def is_hex_code(hex_code: str) -> bool:
        return fullmatch(r"#[0-9A-Fa-f]{6}", hex_code) or fullmatch(r"#[0-9A-Fa-f]{3}", hex_code)

    @staticmethod
    def is_darker(hex_code: str, luminance_threshold: float = DEFAULT_LUMINANCE_THRESHOLD) -> bool:
        red_value, green_value, blue_value = Color.hex_to_rgb(hex_code)
        calculated_luminance: float = Color.luminance(red_value, green_value, blue_value)
        return calculated_luminance < luminance_threshold
