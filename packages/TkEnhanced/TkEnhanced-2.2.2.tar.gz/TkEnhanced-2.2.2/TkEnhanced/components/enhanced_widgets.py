# local imports:
from ..models import TransparentMisc

# standard libraries:
from tkinter import PanedWindow, LabelFrame, Scrollbar, Canvas, Scale, Text


class EnhancedPanedWindow(TransparentMisc, PanedWindow):
    ...


class EnhancedLabelFrame(TransparentMisc, LabelFrame):
    ...


class EnhancedScrollbar(TransparentMisc, Scrollbar):
    ...


class EnhancedCanvas(TransparentMisc, Canvas):
    ...


class EnhancedScale(TransparentMisc, Scale):
    ...


class EnhancedText(TransparentMisc, Text):
    ...
