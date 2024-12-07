# standard libraries:
from dataclasses import dataclass


@dataclass(frozen=True)
class Constants:
    # Special values for widget settings.
    ELLIPSIS: str = "..."
    AUTO: str = "auto"
    DISABLED: str = "disabled"
    READABLE: str = "readable"
    TRANSPARENT: str = "transparent"
    COVER: str = "cover"
    CONTAIN: str = "contain"
    RESIZE_VALUES: tuple[str, ...] = COVER, CONTAIN
    RAISED: str = "raised"
    SUNKEN: str = "sunken"
    FLAT: str = "flat"
    RIDGE: str = "ridge"
    SOLID: str = "solid"
    GROOVE: str = "groove"
    RELIEF_VALUES: tuple[str, ...] = RAISED, SUNKEN, FLAT, RIDGE, SOLID, GROOVE
    HORIZONTAL: str = "horizontal"
    VERTICAL: str = "vertical"
    ORIENTATION_VALUES: tuple[str, ...] = VERTICAL, HORIZONTAL
    ALWAYS: str = "always"
    NEVER: str = "never"
    SHOW_VALUES: tuple[str, ...] = ALWAYS, AUTO, NEVER
    BLURRED: str = "blurred"
    CIRCULAR: str = "circular"
    FILTER_VALUES: tuple[str, ...] = BLURRED, CIRCULAR, DISABLED

    # Keys for background and foreground options.
    BACKGROUND_KEYS: tuple[str, ...] = "background", "bg"
    FOREGROUND_KEYS: tuple[str, ...] = "foreground", "fg"
    HOVER_BACKGROUND_KEYS: tuple[str, ...] = "hoverbackground", "hoverbg"
