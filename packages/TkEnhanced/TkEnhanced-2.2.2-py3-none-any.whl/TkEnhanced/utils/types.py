# standard libraries:
from typing import TypeAlias, Literal, Union, Any
from tkinter.font import Font
from _tkinter import Tcl_Obj
from pathlib import Path

FontDescription: TypeAlias = Union[
    str
    | Font
    | list[Any]
    | tuple[str]
    | tuple[str, int]
    | tuple[str, int, str]
    | tuple[str, int, list[str] | tuple[str, ...]]
    | Tcl_Obj]
PathDescription: TypeAlias = Union[Path, str]
SizeDescription: TypeAlias = Union[str, int]
Relief: TypeAlias = Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
ResizeMode: TypeAlias = Literal["cover", "contain"]
ShowScrollbar: TypeAlias = Literal["always", "auto", "never"]
Orientation: TypeAlias = Literal["horizontal", "vertical"]
ImageFilter: TypeAlias = Literal["blurred", "circular", "disabled"]
