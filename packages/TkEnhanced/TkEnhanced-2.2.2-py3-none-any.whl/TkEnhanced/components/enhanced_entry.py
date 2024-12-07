# local imports:
from ..models import TransparentMisc, ReadableMisc
from ..utils import Relief, Constants, Color

# standard libraries:
from tkinter import Entry, Event, Misc
from typing import Any, Optional


class EnhancedEntry(TransparentMisc, ReadableMisc, Entry):
    @staticmethod
    def get_placeholder_color(enhanced_entry: "EnhancedEntry") -> str:
        if enhanced_entry._placeholder_color != Constants.AUTO:
            return enhanced_entry._placeholder_color
        background: str = Misc.cget(enhanced_entry, key="background")
        background = Color.grant_hex_code(enhanced_entry, hex_code=background)
        return "#cccccc" if Color.is_darker(hex_code=background) else "#aaaaaa"

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            borderwidth: int = 6,
            highlightthickness: Optional[int] = 1,
            placeholdercolor: Optional[str] = Constants.AUTO,
            placeholdertext: str = "",
            relief: Optional[Relief] = Constants.FLAT,
            **options: Any) -> None:
        super().__init__(
            master,
            background=background,
            borderwidth=borderwidth,
            highlightthickness=highlightthickness,
            relief=relief,
            **options)
        self._default_color: Optional[str] = None
        self._default_show: str = ""
        self._placeholder_text: str = ""
        self._placeholder_color: str = Constants.AUTO
        self.configure(placeholdertext=placeholdertext, placeholdercolor=placeholdercolor)
        self.bind(sequence="<FocusIn>", func=self.on_focus, add=True)
        self.bind(sequence="<FocusOut>", func=self.on_blur, add=True)

    def update_foreground(self, event: Optional[Event] = None) -> None:
        placeholder_color: str = self.get_placeholder_color(self)
        if Misc.cget(self, key="foreground") == placeholder_color:
            return None
        super().update_foreground(event)

    def on_focus(self, event: Optional[Event] = None) -> None:
        placeholder_color: str = self.get_placeholder_color(self)
        if Misc.cget(self, key="foreground") != placeholder_color:
            return None
        self.delete(first="0", last="end")
        Misc.configure(self, foreground=self._default_color, show=self._default_show)

    def on_blur(self, event: Optional[Event] = None) -> None:
        if Entry.get(self):
            return None
        placeholder_color: str = self.get_placeholder_color(self)
        Misc.configure(self, foreground=placeholder_color, show="")
        self.insert(index="0", string=self._placeholder_text)

    def configure(self, **options: Any) -> Any:
        if hasattr(self, "_placeholder_color"):
            self.on_focus(event=None)
        placeholder_color: Optional[str] = options.pop("placeholdercolor", None)
        if placeholder_color not in (None, Constants.AUTO):
            self.winfo_rgb(color=placeholder_color)
        placeholder_text: Optional[str] = options.pop("placeholdertext", None)
        result: Any = super().configure(**options)
        if placeholder_text is not None:
            self._placeholder_text = str(placeholder_text)
        if placeholder_color is not None:
            self._placeholder_color = placeholder_color
        self._default_color = Misc.cget(self, key="foreground")
        self._default_show = Misc.cget(self, key="show")
        if not self.focus_get():
            self.after(ms=0, func=self.on_blur)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        options: dict[str, Any] = {
            "placeholdercolor": self._placeholder_color,
            "placeholdertext": self._placeholder_text}
        return options.get(key) if key in options else super().cget(key)
    __getitem__ = cget

    def set(self, value: str) -> None:
        self.on_focus(event=None)
        self.delete(first="0", last="end")
        self.insert(index="0", string=value)
        if not self.focus_get():
            self.on_blur(event=None)

    def get(self) -> str:
        placeholder_color: str = self.get_placeholder_color(self)
        return "" if Misc.cget(self, key="foreground") == placeholder_color else super().get()
