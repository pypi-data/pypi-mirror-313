# local imports:
from ..utils import Constants

# standard libraries:
from tkinter import BaseWidget, Event, Misc
from typing import Any, Optional


class TransparentMisc(Misc):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            **options: Any) -> None:
        assert isinstance(self, BaseWidget), "This object must be an instance of BaseWidget class."
        background = options.pop("bg", background)
        super().__init__(master, **options)
        self._background: str = Constants.TRANSPARENT
        self.configure(background=background)
        self.bind(sequence="<<ParentUpdate>>", func=self.on_parent_update, add=True)

    def on_parent_update(self, event: Event) -> None:
        if self._background != Constants.TRANSPARENT:
            return None
        parent_background: str = Misc.cget(self.master, key="background")
        if not parent_background:
            return None
        Misc.configure(self, background=parent_background)
        self.event_generate(sequence="<<UpdateForeground>>", when="tail")
        self.event_generate(sequence="<<UpdatePalette>>", when="now")
        self.update_children()

    def update_children(self) -> None:
        for child_widget in self.winfo_children():
            child_widget.event_generate(sequence="<<ParentUpdate>>", when="now")

    def configure(self, **options: Any) -> Any:
        background: Optional[str] = options.pop("background", None)
        background = options.pop("bg", background)
        is_transparent: bool = background == Constants.TRANSPARENT
        if is_transparent:
            background = Misc.cget(self.master, key="background")
        options["background"] = background
        result: Any = super().configure(**options)
        if background is not None:
            self._background = Constants.TRANSPARENT if is_transparent else background
            self.after(ms=0, func=self.update_children)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        return self._background if key in Constants.BACKGROUND_KEYS else super().cget(key)
    __getitem__ = cget
