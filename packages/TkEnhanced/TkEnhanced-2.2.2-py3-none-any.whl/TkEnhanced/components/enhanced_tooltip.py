# local imports:
from ..models import TransparentMisc
from ..utils import Constants
from . import EnhancedLabel

# standard libraries:
from tkinter import Toplevel, Event, Misc
from typing import Any, Optional


class EnhancedTooltip(Toplevel):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            text: Optional[str] = "Enhanced Tooltip",
            **options: Any) -> None:
        super().__init__(master, **options)
        self.setup_tooltip(text)
        self.master.bind(sequence="<Enter>", func=self.show_tooltip, add=True)
        self.master.bind(sequence="<Motion>", func=self.update_position, add=True)
        self.master.bind(sequence="<Leave>", func=self.hide_tooltip, add=True)

    def setup_tooltip(self, text: Optional[str] = None) -> None:
        self.wm_withdraw()
        self.wm_title(string=text)
        self.wm_overrideredirect(boolean=True)
        self.configure(padx=2, pady=2)
        self._label: EnhancedLabel = EnhancedLabel(self, text=text, truncatetext=False)
        self._label.pack_configure(expand=True, fill="both")

    def show_tooltip(self, event: Event) -> None:
        self.update_idletasks()
        self.wm_deiconify()
        self.after(20, self.update_position, event)

    def update_position(self, event: Event) -> None:
        tooltip_width: int = self.winfo_reqwidth()
        x_position: int = event.x_root-tooltip_width//2
        y_position: int = event.y_root-40
        new_position: str = "+{}+{}".format(x_position, y_position)
        self.wm_geometry(newGeometry=new_position)

    def hide_tooltip(self, event: Event) -> None:
        self.wm_withdraw()

    def configure(self, **options: Any) -> Any:
        text: Optional[str] = options.pop("text", None)
        if text is not None:
            self._label.configure(text=text)
        result: Any = super().configure(**options)
        if Constants.BACKGROUND_KEYS & options.keys():
            def update_children() -> None: TransparentMisc.update_children(self)
            self.after(ms=0, func=update_children)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        return self._label.cget(key="text") if key == "text" else super().cget(key)
    __getitem__ = cget
