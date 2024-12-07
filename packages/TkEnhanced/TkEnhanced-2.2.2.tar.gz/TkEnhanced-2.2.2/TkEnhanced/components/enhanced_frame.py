# local imports:
from ..models import TransparentMisc, HoverMisc
from ..utils import Constants

# standard libraries:
from typing import Any, Optional
from tkinter import Frame, Misc


class EnhancedFrame(TransparentMisc, HoverMisc, Frame):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            hoverbackground: Optional[str] = Constants.DISABLED,
            **options: Any) -> None:
        super().__init__(master, background=background, hoverbackground=hoverbackground, **options)
        if hoverbackground != Constants.DISABLED and background not in (Constants.AUTO, Constants.TRANSPARENT):
            self._palette_colors[0] = background
