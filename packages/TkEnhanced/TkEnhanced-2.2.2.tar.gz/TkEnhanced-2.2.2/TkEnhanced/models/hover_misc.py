# local imports:
from ..utils import Constants, Color

# standard libraries:
from tkinter import TclError, EventType, Widget, Event, Misc
from typing import Any, Optional


class HoverMisc(Misc):
    PALETTE_SIZE: int = 12
    PALETTE_UPDATE_MILLISECONDS: int = 6

    @staticmethod
    def is_hover_background(master: Misc, hover_background: str) -> bool:
        try:
            master.winfo_rgb(color=hover_background)
            return True
        except TclError:
            if hover_background in (Constants.AUTO, Constants.DISABLED):
                return True
            return False

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            hoverbackground: Optional[str] = Constants.AUTO,
            **options: Any) -> None:
        assert isinstance(self, Widget), "This object must be an instance of Widget class."
        hover_background: Optional[str] = options.pop("hoverbg", hoverbackground)
        super().__init__(master, **options)
        self._hover_background: Optional[str] = Constants.DISABLED
        self._palette_colors: list[str] = []
        self._palette_index: int = 0
        self._palette_index_update: Optional[str] = None
        self._binded_widgets: set[Misc] = set()
        self.bind(sequence="<<UpdatePalette>>", func=self.update_palette, add=True)
        self.configure(hoverbackground=hover_background)
        self.bind(sequence="<Enter>", func=self.on_mouse_interact, add=True)
        self.bind(sequence="<Leave>", func=self.on_mouse_interact, add=True)

    def on_mouse_interact(self, event: Event) -> None:
        if self._palette_index_update is not None:
            self.after_cancel(id=self._palette_index_update)
            self._palette_index_update = None
        is_mouse_hover: bool = event.type == EventType.Enter
        palette_index: int = self._palette_index + (1 if is_mouse_hover else -1)
        palette_index = min(len(self._palette_colors)-1, max(0, palette_index))
        if palette_index == self._palette_index:
            return None
        self._palette_index = palette_index
        self.after(ms=0, func=self.update_background)
        self._palette_index_update = self.after(self.PALETTE_UPDATE_MILLISECONDS, self.on_mouse_interact, event)

    def update_background(self) -> None:
        if not self._palette_colors or self._hover_background == Constants.DISABLED:
            return None
        background: str = self._palette_colors[self._palette_index]
        Misc.configure(self, background=background)
        self.event_generate(sequence="<<UpdateForeground>>", when="now")
        for child_widget in self.winfo_children():
            child_widget.event_generate(sequence="<<ParentUpdate>>", when="now")

    def update_palette(self, event: Optional[Event] = None) -> None:
        if self._hover_background == Constants.DISABLED:
            return None
        background: str = Misc.cget(self, key="background") \
            if event is not None or not self._palette_colors else \
            self._palette_colors[0]
        background = Color.grant_hex_code(self, hex_code=background)
        hover_background: str = self._hover_background
        if hover_background == Constants.AUTO:
            brightness_factor: float = 1.6 if Color.is_darker(hex_code=background) else .6
            hover_background = Color.adjust_brightness(hex_code=background, factor=brightness_factor)
        hover_background = Color.grant_hex_code(self, hex_code=hover_background)
        self._palette_colors = Color.generate_palette(
            start_hex=background,
            end_hex=hover_background,
            num_colors=self.PALETTE_SIZE)
        self.after(ms=0, func=self.update_background)

    def configure(self, **options: Any) -> Any:
        hover_background: Optional[str] = options.pop("hoverbackground", None)
        hover_background = options.pop("hoverbg", hover_background)
        if hover_background is not None and not self.is_hover_background(self, hover_background):
            error_message: str = "unknown color name \"{}\"".format(hover_background)
            raise TclError(error_message)
        result: Any = super().configure(**options)
        if hover_background is not None:
            self._hover_background = hover_background
        background: Optional[str] = options.get("background", None)
        background = options.get("bg", background)
        if background is not None:
            self.event_generate(sequence="<<UpdatePalette>>", when="now")
        elif hover_background is not None:
            self.after(ms=0, func=self.update_palette)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        return self._hover_background if key in Constants.HOVER_BACKGROUND_KEYS else super().cget(key)
    __getitem__ = cget
