# local imports:
from ..models import TransparentMisc, ReadableMisc, HoverMisc
from ..utils import Constants, Color

# standard libraries:
from tkinter import Button, Event, Misc
from typing import Any, Optional


class EnhancedButton(TransparentMisc, ReadableMisc, HoverMisc, Button):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            borderwidth: Optional[int] = 1,
            foreground: Optional[str] = Constants.READABLE,
            highlightthickness: Optional[int] = 5,
            hoverbackground: Optional[str] = Constants.AUTO,
            text: Optional[str] = "Enhanced Button",
            **options: Any) -> None:
        super().__init__(
            master,
            background=background,
            borderwidth=borderwidth,
            foreground=foreground,
            highlightthickness=highlightthickness,
            hoverbackground=hoverbackground,
            text=text,
            **options)

    def update_palette(self, event: Optional[Event] = None) -> None:
        if self._hover_background == Constants.DISABLED:
            return None
        background: str = Misc.cget(self, key="background") \
            if event is not None or not self._palette_colors else \
            self._palette_colors[0]
        background = Color.grant_hex_code(self, hex_code=background)
        hover_background: str = self._hover_background
        if hover_background == Constants.AUTO:
            active_background: str = Misc.cget(self, key="activebackground")
            active_background = Color.grant_hex_code(self, hex_code=active_background)
            brightness_factor: float = 1.2 if Color.is_darker(hex_code=active_background) else .8
            hover_background = Color.adjust_brightness(hex_code=active_background, factor=brightness_factor)
        hover_background = Color.grant_hex_code(self, hex_code=hover_background)
        self._palette_colors = Color.generate_palette(
            start_hex=background,
            end_hex=hover_background,
            num_colors=self.PALETTE_SIZE)
        self.after(ms=0, func=self.update_background)

    def configure(self, **options: Any) -> Any:
        result: Any = super().configure(**options)
        if "activebackground" in options:
            self.after(ms=0, func=self.update_palette)
        return result
    config = configure
