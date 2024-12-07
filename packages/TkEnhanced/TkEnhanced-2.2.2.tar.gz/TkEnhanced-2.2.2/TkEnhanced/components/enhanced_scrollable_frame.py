# local imports:
from . import EnhancedScrollbar, EnhancedCanvas, EnhancedFrame
from ..utils import ShowScrollbar, Orientation, Constants

# standard libraries:
from typing import Any, Callable, Optional
from tkinter import TclError, Event, Misc


class EnhancedScrollableFrame(EnhancedFrame):
    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            showscrollbar: ShowScrollbar = Constants.AUTO,
            orient: Orientation = Constants.VERTICAL,
            **options: Any) -> None:
        super().__init__(master, background=background, **options)
        self._binded_widgets: set[Misc] = set()
        self._show_scrollbar: ShowScrollbar = Constants.AUTO
        self._orientation: Orientation = Constants.VERTICAL
        self.setup_widgets()
        self.configure(showscrollbar=showscrollbar, orient=orient)
        self.bind(sequence="<Configure>", func=self.move_children, add=True)

    def move_children(self, event: Event) -> None:
        for child_widget in self.winfo_children() + self.frame_in.winfo_children():
            if child_widget in (self._canvas, self._scrollbar):
                continue
            self.bind_mouse_wheel(widget=child_widget)
            configure_command: Optional[Callable] = child_widget.grid_configure if child_widget.grid_info() \
                else child_widget.pack_configure if child_widget.pack_info() \
                else child_widget.place_configure if child_widget.place_info() else None
            configure_command(in_=self.frame_in)
        self.update_scrollbar()

    def bind_mouse_wheel(self, widget: Misc) -> None:
        if widget not in self._binded_widgets:
            widget.bind(sequence="<MouseWheel>", func=self.on_mouse_wheel, add=True)
            self._binded_widgets.add(widget)
        for child_widget in widget.winfo_children():
            self.bind_mouse_wheel(widget=child_widget)

    def setup_widgets(self) -> None:
        self._scrollbar: EnhancedScrollbar = EnhancedScrollbar(self, borderwidth=0, orient="vertical")
        self._canvas: EnhancedCanvas = EnhancedCanvas(
            master=self,
            highlightthickness=0,
            xscrollcommand=self._scrollbar.set,
            yscrollcommand=self._scrollbar.set)
        self._canvas.bind(sequence="<MouseWheel>", func=self.on_mouse_wheel, add=True)
        self._canvas.bind(sequence="<Configure>", func=self.on_configure, add=True)
        self._canvas.pack_configure(expand=True, fill="both")
        self.frame_in: EnhancedFrame = EnhancedFrame(self._canvas)
        self.frame_in.bind(sequence="<MouseWheel>", func=self.on_mouse_wheel, add=True)
        self.frame_in.bind(sequence="<Configure>", func=self.on_configure, add=True)
        self.frame_id: int = self._canvas.create_window(0, 0, anchor="nw", window=self.frame_in)

    def on_mouse_wheel(self, event: Event) -> None:
        if self._scrollbar.get() == (.0, 1.):
            return None
        scroll_commands: dict[str, Callable] = {
            "vertical": self._canvas.yview_scroll,
            "horizontal": self._canvas.xview_scroll}
        scroll_command: Optional[Callable] = scroll_commands.get(self._orientation, None)
        if scroll_command is None:
            return None
        scroll_amount: int = event.delta // 120
        scroll_command(number=-scroll_amount, what="units")

    def on_configure(self, event: Event) -> None:
        scroll_coordinates: tuple[int, int, int, int] = self._canvas.bbox("all")
        scroll_coordinates: list[int] = list(scroll_coordinates)
        canvas_end_x, canvas_end_y = scroll_coordinates[2:]
        canvas_width, canvas_height = event.width, event.height
        scroll_coordinates[2] = max(canvas_end_x, canvas_width)
        scroll_coordinates[3] = max(canvas_end_y, canvas_height)
        self._canvas.configure(scrollregion=scroll_coordinates)
        is_vertical: bool = self._orientation == "vertical"
        height: int = 0 if is_vertical else canvas_height
        width: int = canvas_width if is_vertical else 0
        self._canvas.itemconfigure(tagOrId=self.frame_id, height=height, width=width)
        self.update_scrollbar()

    def update_scrollbar(self) -> None:
        self._scrollbar.update_idletasks()
        if self._show_scrollbar == "never" or self._show_scrollbar == "auto" and self._scrollbar.get() == (.0, 1.):
            self._scrollbar.pack_forget()
            return None
        sides: dict[str, str] = {"vertical": "right", "horizontal": "bottom"}
        side: Optional[str] = sides.get(self._orientation, None)
        self._scrollbar.pack_configure(before=self._canvas, fill="both", side=side)

    def configure(self, **options: Any) -> Any:
        show_scrollbar: Optional[ShowScrollbar] = options.pop("showscrollbar", None)
        if show_scrollbar not in (None, *Constants.SHOW_VALUES):
            error_message: str = "bad state \"{}\": must be {}, {} or {}".format(orientation, *Constants.SHOW_VALUES)
            raise TclError(error_message)
        orientation: Optional[Orientation] = options.pop("orient", None)
        if orientation not in (None, *Constants.ORIENTATION_VALUES):
            error_message: str = "bad orientation \"{}\": must be {} or {}".format(
                orientation,
                *Constants.ORIENTATION_VALUES)
            raise TclError(error_message)
        result: Any = super().configure(**options)
        if show_scrollbar is not None:
            self._show_scrollbar = show_scrollbar
        if orientation is not None:
            self._orientation = orientation
            commands: dict[str, Callable] = {"vertical": self._canvas.yview, "horizontal": self._canvas.xview}
            command: Optional[Callable] = commands.get(self._orientation, None)
            self._scrollbar.configure(command=command, orient=self._orientation)
        return result
    config = configure

    def cget(self, key: str) -> Any:
        return self._orientation if key == "orient" else super().cget(key)
    __getitem__ = cget
