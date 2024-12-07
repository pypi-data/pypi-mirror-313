# local imports:
from ..utils import FontDescription,Constants
from . import EnhancedFrame, EnhancedLabel

# standard libraries:
from typing import Any, LiteralString,Optional
from tkinter.font import Font
from tkinter import Misc


class EnhancedCheckbutton(EnhancedFrame):
    CHECKED_UNICODE_CHAR:LiteralString="\u2611"
    UNCHECKED_UNICODE_CHAR:LiteralString="\u2610"
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            font:Optional[FontDescription]=None,
            foreground: Optional[str] = Constants.READABLE,
            text: Optional[str] = "Enhanced Checkbutton",
            truncatetext: bool = True,
            **options: Any) -> None:
        super().__init__(master, background=background, **options)
        self._value:bool=False
        self.setup_widgets()
        self.configure(font=font,foreground=foreground,text=text, truncatetext=truncatetext)
        self.bind(sequence="<Button-1>",func=lambda _: self.toggle(),add=True)

    def setup_widgets(self)->None:
        # create widgets:
        self.value_label:EnhancedLabel=EnhancedLabel(
            master=self,
            padx=0,
            text=self.UNCHECKED_UNICODE_CHAR,
            truncatetext=False)
        self.value_label.bind(sequence="<Button-1>",func=lambda _: self.toggle(),add=True)
        self.text_label:EnhancedLabel=EnhancedLabel(self)
        self.text_label.bind(sequence="<Button-1>",func=lambda _: self.toggle(),add=True)
        # display user interface elements:
        self.value_label.pack_configure(fill="y", side="left")
        self.text_label.pack_configure(expand=True, fill="both", side="right")

    def configure(self, **options: Any) -> Any:
        font:Optional[FontDescription]=options.pop("font",None)
        if font is not None:
            self.value_label.configure(font=font)
            self.text_label.configure(font=font)
        foreground:Optional[str]=options.pop("foreground",None)
        if foreground is not None:
            self.value_label.configure(foreground=foreground)
            self.text_label.configure(foreground=foreground)
        text:Optional[str]=options.pop("text",None)
        truncate_text:Optional[bool]=options.pop("truncatetext",None)
        if text is not None or truncate_text is not None:
            self.text_label.configure(text=text, truncatetext=truncate_text)
        return super().configure(**options)

    def get(self)->bool:
        return self._value

    def set(self, new_state:bool)->None:
        if not isinstance(new_state,bool):
            raise ValueError("\"new_state\" must be a boolean value.")
        new_text:str=self.CHECKED_UNICODE_CHAR if new_state else self.UNCHECKED_UNICODE_CHAR
        self.value_label.configure(text=new_text)
        self._value = new_state

    def toggle(self)->bool:
        current_state:bool=self.get()
        new_state:bool=not current_state
        self.set(new_state)
        return new_state
