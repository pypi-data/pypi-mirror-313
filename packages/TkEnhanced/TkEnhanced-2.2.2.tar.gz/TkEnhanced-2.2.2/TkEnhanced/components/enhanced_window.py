# local imports:
from ..models import TransparentMisc
from ..utils import Constants

# standard libraries:
from tkinter import Toplevel, Event, Misc, Wm, Tk
from ctypes import windll, WinDLL, byref
from ctypes.wintypes import POINT, RECT
from typing import Any, Optional
from enum import IntEnum


class WindowIndexes(IntEnum):
    WINDOW_STYLE: int = -16
    EXTENDED_WINDOW_STYLE: int = -20


class WindowStyles(IntEnum):
    MAXIMIZE: int = 0x00010000
    MINIMIZE: int = 0x00020000
    RESIZE: int = 0x00040000


class ExtendedWindowStyles(IntEnum):
    TASKBAR: int = 0x00040000


class MotionUtils:
    def __init__(self, master: "WindowUtils") -> None:
        assert isinstance(master, WindowUtils), "The parent master must be an instance of WindowUtils."
        self.master: WindowUtils = master
        self.start_x: Optional[int] = None
        self.start_y: Optional[int] = None

    def start_move(self, event: Event) -> None:
        current_state: str = self.master.master.wm_state()
        x_screen: int = event.x_root
        y_screen: int = event.y_root
        x_window: int = self.master.master.winfo_rootx()
        y_window: int = self.master.master.winfo_rooty()
        self.master.master.wm_state(newstate="normal")
        self.start_x = (x_screen-x_window) % self.master.master.winfo_width()
        self.start_y = (y_screen-y_window) % self.master.master.winfo_height()
        self.master.master.wm_state(newstate=current_state)

    def on_move(self, event: Event) -> None:
        if None in (self.start_x,self.start_y):
            return None
        cursor_position: POINT = POINT()
        cursor_position_handler: int = byref(cursor_position)
        self.master._windows_api.GetCursorPos(cursor_position_handler)
        window_handle: int = self.master.retrieve_window_handle()
        self.master._windows_api.ScreenToClient(window_handle, cursor_position_handler)
        window_rectangle: RECT = RECT()
        window_rectangle_handler: int = byref(window_rectangle)
        self.master._windows_api.GetWindowRect(window_handle, window_rectangle_handler)
        new_y: int = self.master.master.winfo_y()+(cursor_position.y-self.start_y)
        if new_y <= 0:
            resizable: tuple[bool, bool] = self.master.master.wm_resizable()
            if not any(not resizable for resizable in resizable):
                if self.master.master.wm_state() == "normal":
                    self.master.master.wm_state(newstate="zoomed")
                return None
        elif self.master.master.wm_state() == "zoomed":
            self.master.master.wm_state(newstate="normal")
            self.on_move(event)
            return None
        new_x: int = self.master.master.winfo_x()+(cursor_position.x-self.start_x)
        width: int = window_rectangle.right-window_rectangle.left
        height: int = window_rectangle.bottom-window_rectangle.top
        self.master._windows_api.SetWindowPos(window_handle, None, new_x, new_y, width, height, 1)

    def stop_move(self, event: Event) -> None:
        self.start_x = self.start_y = None


class WindowUtils:
    _graphics_api: WinDLL = windll.gdi32
    _windows_api: WinDLL = windll.user32

    def __init__(self, master: "EnhancedWindow") -> None:
        assert isinstance(master, EnhancedWindow), "This object must be an instance of EnhancedWindow."
        self.master: EnhancedWindow = master
        self._motion_utils: MotionUtils = MotionUtils(self)
        self._updated_size: tuple[int, int] = 0, 0
        self._updated_styles: dict[int, int] = {}

    def on_configure(self, event: Event) -> None:
        if self._updated_size == (event.width, event.height):
            return None
        self._updated_size = event.width, event.height
        if event.widget != self.master or not self.master.wm_overrideredirect():
            return None
        window_id: int = self.retrieve_window_handle()
        is_width_resizable, is_height_resizable = self.master.wm_resizable()
        start_x: int = 6 if is_width_resizable else 7
        start_y: int = 6 if is_height_resizable else 7
        end_x: int = event.width+(8 if is_width_resizable else 7)
        end_y: int = event.height+(8 if is_height_resizable else 7)
        if self.master.wm_state() == "zoomed" and not is_width_resizable:
            end_x -= 1
        new_region: int = self._graphics_api.CreateRectRgn(start_x, start_y, end_x, end_y)
        self._windows_api.SetWindowRgn(window_id, new_region, True)

    def bind_motion(self, widget: Misc) -> None:
        widget.bind(sequence="<Button-1>", func=self._motion_utils.start_move, add=True)
        widget.bind(sequence="<Button1-Motion>", func=self._motion_utils.on_move, add=True)
        widget.bind(sequence="<ButtonRelease-1>", func=self._motion_utils.stop_move, add=True)
        widget.bind(sequence="<Double-Button-1>", func=lambda event: self.toggle_maximize(), add=True)

    def retrieve_window_handle(self) -> int:
        self.master.update_idletasks()
        window_id: int = self.master.winfo_id()
        window_handle: int = self._windows_api.GetParent(window_id)
        return window_handle

    def center_window(self, width: int, height: int) -> None:
        screen_width: int = self.master.winfo_screenwidth()
        screen_height: int = self.master.winfo_screenheight()
        center_x: int = (screen_width-width)//2
        center_y: int = (screen_height-height)//2
        new_geometry: str = "{}x{}+{}+{}".format(width, height, center_x, center_y)
        self.master.wm_geometry(newGeometry=new_geometry)

    def hide_titlebar(self) -> None:
        if self.master.wm_overrideredirect():
            return None
        self.master.wm_overrideredirect(boolean=True)
        window_handle: int = self.retrieve_window_handle()
        self._updated_styles[WindowIndexes.WINDOW_STYLE] = self._windows_api.GetWindowLongPtrW(
            window_handle,
            WindowIndexes.WINDOW_STYLE)
        self._updated_styles[WindowIndexes.EXTENDED_WINDOW_STYLE] = self._windows_api.GetWindowLongPtrW(
            window_handle,
            WindowIndexes.EXTENDED_WINDOW_STYLE)
        new_styles: dict[int, int] = {
            WindowIndexes.WINDOW_STYLE: WindowStyles.MAXIMIZE | WindowStyles.MINIMIZE | WindowStyles.RESIZE,
            WindowIndexes.EXTENDED_WINDOW_STYLE: ExtendedWindowStyles.TASKBAR}
        for index, style in new_styles.items():
            self._windows_api.SetWindowLongPtrW(window_handle, index, style)
        is_window_shown: bool = self.master.wm_state() != "withdrawn"
        if is_window_shown:
            self.master.wm_deiconify()

    def show_titlebar(self) -> None:
        if not self.master.wm_overrideredirect():
            return None
        window_handle: int = self.retrieve_window_handle()
        for index, style in self._updated_styles.items():
            self._windows_api.SetWindowLongPtrW(window_handle, index, style)
        self._updated_styles.clear()
        self.master.wm_overrideredirect(boolean=False)

    def toggle_maximize(self) -> None:
        resizable: tuple[bool, bool] = self.master.wm_resizable()
        if any(not resizable for resizable in resizable):
            return None
        new_state: str = "zoomed" if self.master.wm_state() == "normal" else "normal"
        self.master.wm_state(new_state)

    def minimize_window(self) -> None:
        is_titlebar_hidden: bool = self.master.wm_overrideredirect()
        if is_titlebar_hidden:
            window_handle: int = self.retrieve_window_handle()
            self._windows_api.ShowWindow(window_handle, 6)
            return None
        self.master.wm_iconify()
    minimize = minimize_window


class EnhancedWindow(Misc, Wm):
    def __init__(self, **options: Any) -> None:
        super().__init__(**options)
        self.utils: WindowUtils = WindowUtils(self)
        self.bind(sequence="<Configure>", func=self.utils.on_configure, add=True)

    def configure(self, **options: Any) -> Any:
        result: Any = super().configure(**options)
        if Constants.BACKGROUND_KEYS & options.keys():
            def update_children() -> None: TransparentMisc.update_children(self)
            self.after(ms=0, func=update_children)
        return result
    config = configure


class EnhancedTk(EnhancedWindow, Tk):
    def __init__(self, *, className: str = "TkEnhanced", **options: Any) -> None:
        super().__init__(className=className, **options)


class EnhancedToplevel(EnhancedWindow, Toplevel):
    def __init__(self, master: Optional[Misc] = None, *, modal: bool = False, **options: Any) -> None:
        super().__init__(master=master, **options)
        if modal:
            self.grab_set()
            self.master.wait_window(self)
            self.grab_release()
