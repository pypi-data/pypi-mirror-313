# local imports:
from ..utils import Constants, Color

# standard libraries:
from tkinter import Widget, Event, Misc
from typing import Any, Optional


class ReadableMisc(Misc):
    @staticmethod
    def get_foreground(master: Misc, **options: Any) -> str:
        background: Optional[str] = options.get("background", None)
        background = options.get("bg", background)
        if background is None:
            background = Misc.cget(master, key="background")
        background = Color.grant_hex_code(master, hex_code=background)
        foreground: str = "#ffffff" if Color.is_darker(background) else "#000000"
        return foreground

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            foreground: Optional[str] = Constants.READABLE,
            **options: Any) -> None:
        assert isinstance(self, Widget), "This object must be an instance of Widget class."
        foreground: Optional[str] = options.pop("fg", foreground)
        super().__init__(master, **options)
        self._foreground: str = Constants.READABLE
        self.configure(foreground=foreground)
        self.bind(sequence="<<UpdateForeground>>", func=self.update_foreground, add=True)

    def update_foreground(self, event: Optional[Event] = None) -> None:
        foreground: str = self.get_foreground(self) \
            if self._foreground == Constants.READABLE or hasattr(self, "_palette_index") and self._palette_index \
            else self._foreground
        Misc.configure(self, foreground=foreground)

    def configure(self, **options: Any) -> Any:
        foreground: Optional[str] = options.pop("foreground", None)
        foreground = options.pop("fg", foreground)
        is_readable: bool = foreground == Constants.READABLE
        if is_readable:
            foreground = self.get_foreground(self, **options)
        options["foreground"] = foreground
        result: Any = super().configure(**options)
        if foreground is not None:
            self._foreground = Constants.READABLE if is_readable else foreground
            self.after(ms=0, func=self.update_foreground)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        return self._foreground if key in Constants.FOREGROUND_KEYS else super().cget(key)
    __getitem__ = cget
