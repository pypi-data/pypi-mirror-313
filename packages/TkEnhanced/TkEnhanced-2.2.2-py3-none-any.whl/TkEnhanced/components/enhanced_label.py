# local imports:
from ..models import TransparentMisc, ReadableMisc
from ..utils import FontDescription, Constants

# standard libraries:
from tkinter import Event, Label, Misc
from typing import Any, Optional
from tkinter.font import Font


class EnhancedLabel(TransparentMisc, ReadableMisc, Label):
    MINIMUM_PADDING_X: int = 5

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            foreground: Optional[str] = Constants.READABLE,
            padx: Optional[int] = MINIMUM_PADDING_X,
            text: Optional[str] = "Enhanced Label",
            truncatetext: bool = True,
            **options: Any) -> None:
        self._truncate_text: bool = False
        self._text: str = ""
        super().__init__(master, background=background, foreground=foreground, **options)
        self.configure(padx=padx, text=text, truncatetext=truncatetext)
        self.bind(sequence="<Configure>", func=self.on_configure, add=True)

    def on_configure(self, event: Optional[Event] = None) -> None:
        if not self._truncate_text:
            Misc.configure(self, text=self._text)
            return None
        self.update_idletasks()
        font: FontDescription = self.cget(key="font")
        font = Font(font=font)
        label_width: int = self.winfo_width()
        minimum_width: int = font.measure(text=Constants.ELLIPSIS)
        if minimum_width > label_width:
            Misc.configure(self, text=Constants.ELLIPSIS)
            return None
        text: str = self._text
        text_width: int = font.measure(text)
        if text_width > label_width:
            while font.measure(text=text+Constants.ELLIPSIS) > label_width:
                text = text[:-1]
            text += Constants.ELLIPSIS
        Misc.configure(self, text=text)

    def configure(self, **options: Any) -> Any:
        truncate_text: Optional[bool] = options.pop("truncatetext", self._truncate_text)
        padding_x: Optional[int] = options.get("padx", None)
        if isinstance(padding_x, int) and padding_x < self.MINIMUM_PADDING_X and truncate_text:
            error_message: str = "number of \"padx\" must be at least {}.".format(self.MINIMUM_PADDING_X)
            raise ValueError(error_message)
        result: Any = super().configure(**options)
        if truncate_text is not None:
            self._truncate_text = bool(truncate_text)
            if self._truncate_text and self["padx"] < self.MINIMUM_PADDING_X:
                Misc.configure(self, padx=self.MINIMUM_PADDING_X)
        text: Optional[str] = options.get("text", None)
        if text is not None:
            self._text = str(text)
            self.after(ms=0, func=self.on_configure)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        options: dict[str, Any] = {"text": self._text, "truncatetext": self._truncate_text}
        return options.get(key) if key in options else super().cget(key)
    __getitem__ = cget
