# local imports:
from ..models import TransparentMisc
from ..utils import Constants

# standard libraries:
from tkinter import TclError, Toplevel, Event, Misc
from typing import Any, Optional


class EnhancedSidebar(Toplevel):
    @staticmethod
    def check_options(**options: Any) -> None:
        unknown_options: tuple[str, ...] = "height", "width"
        for option in unknown_options:
            if option not in options:
                continue
            error_message: str = "unknown option \"{}\"".format(option)
            raise TclError(error_message)

    def __init__(self, master: Optional[Misc] = None, **options: Any) -> None:
        self.check_options(**options)
        super().__init__(master, **options)
        self.wm_overrideredirect(boolean=True)
        self.hide()
        self.pack_propagate(flag=False)
        self.bind(sequence="<FocusOut>", func=self.hide, add=True)

    def configure(self, **options: Any) -> Any:
        self.check_options(**options)
        result: Any = super().configure(**options)
        if Constants.BACKGROUND_KEYS & options.keys():
            def update_children() -> None: TransparentMisc.update_children(self)
            self.after(ms=0, func=update_children)
        return result
    config = configure

    def show(self, event: Optional[Event] = None) -> None:
        self.master.update_idletasks()
        width: int = self.master.winfo_width()//2
        height: int = self.master.winfo_height()
        x_position: int = self.master.winfo_rootx()
        y_position: int = self.master.winfo_rooty()
        new_geometry: str = "{}x{}+{}+{}".format(width, height, x_position, y_position)
        self.wm_geometry(newGeometry=new_geometry)
        self.wm_deiconify()
        self.focus_force()

    def hide(self, event: Optional[Event] = None) -> None:
        self.wm_withdraw()
