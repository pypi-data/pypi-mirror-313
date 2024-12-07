# local imports:
from ..utils import PathDescription, SizeDescription, ImageFilter, ResizeMode, Constants
from ..models import TransparentMisc

# standard libraries:
from tkinter import TclError, Event, Label, Misc
from typing import Any, Optional, Callable
from dataclasses import dataclass
from threading import Thread
from os.path import exists

# third-party libraries:
from PIL.Image import Image, open as open_image, new as create_image
from PIL.ImageDraw import ImageDraw, Draw as draw_image
from PIL.ImageFilter import GaussianBlur
from PIL.ImageTk import PhotoImage


@dataclass(frozen=True)
class ImageProcessor:
    @staticmethod
    def blur_image(image: Image, container_size: int) -> Image:
        blur_filter: GaussianBlur = GaussianBlur(radius=60)
        blurred_image_size: tuple[int, int] = container_size, container_size
        blurred_image: Image = image.resize(size=blurred_image_size).filter(filter=blur_filter)
        new_image: Image = create_image(mode="RGB", size=blurred_image_size)
        new_image.paste(blurred_image)
        x_offset: int = (new_image.width-image.width)//2
        y_offset: int = (new_image.height-image.height)//2
        new_image.paste(im=image, box=(x_offset, y_offset), mask=image)
        return new_image

    @staticmethod
    def make_image_circular(image: Image, container_size: int) -> Image:
        left: float = image.width/2-container_size/2
        upper: float = image.height/2-container_size/2
        right: float = image.width/2+container_size/2
        lower: float = image.height/2+container_size/2
        crop_rectangle: tuple[float, float, float, float] = left, upper, right, lower
        cropped_image = image.crop(box=crop_rectangle)
        cropped_image_size: tuple[int, int] = cropped_image.size
        circle_mask = create_image(mode="L", size=cropped_image_size, color=0)
        draw: ImageDraw = draw_image(im=circle_mask)
        draw_coords: tuple[int, int, int, int] = 0, 0, *cropped_image_size
        draw.ellipse(xy=draw_coords, fill=255)
        circular_image: Image = create_image(mode="RGBA", size=cropped_image_size)
        circular_image.paste(im=cropped_image, box=(0, 0), mask=circle_mask)
        return circular_image


class EnhancedImage(TransparentMisc, Label):
    UPDATE_MILLISECONDS: int = 20

    @staticmethod
    def check_options(**options: Any) -> None:
        unknown_options: tuple[str, ...] = "activeforeground", "bitmap", "disabledforeground", "font", "foreground", "takefocus", "text", "textvariable", "underline", "wraplength"
        for option in unknown_options:
            if option not in options:
                continue
            error_message: str = "unknown option \"{}\"".format(option)
            raise TclError(error_message)
        image_filter: Optional[ImageFilter] = options.get("filter", None)
        if image_filter is not None and image_filter not in Constants.FILTER_VALUES:
            error_message: str = "invalid image filter \"{}\": must be {}, {} or {}".format(
                image_filter,
                *Constants.FILTER_VALUES)
            raise TclError(error_message)
        height: Optional[SizeDescription] = options.get("height", None)
        if height not in (None, Constants.AUTO) and not isinstance(height, int):
            error_message: str = "expected \"auto\" or integer but got \"{}\"".format(height)
            raise TclError(error_message)
        image_path: Optional[PathDescription] = options.get("image", None)
        if image_path and not exists(path=image_path):
            error_message: str = "image not found: \"{}\"".format(image_path)
            raise TclError(error_message)
        resize_mode: Optional[ResizeMode] = options.get("resizemode", None)
        if resize_mode is not None and resize_mode not in Constants.RESIZE_VALUES:
            error_message: str = "invalid resize mode \"{}\": must be {} or {}".format(
                resize_mode,
                *Constants.RESIZE_VALUES)
            raise TclError(error_message)
        width: Optional[SizeDescription] = options.get("width", None)
        if width not in (None, Constants.AUTO) and not isinstance(width, int):
            error_message: str = "expected \"auto\" or integer but got \"{}\"".format(width)
            raise TclError(error_message)

    @staticmethod
    def calculate_size(container: "EnhancedImage", image: Image) -> tuple[int, int]:
        image_width, image_height = image.size
        container_width: int = container.winfo_width()
        container_height: int = container.winfo_height()
        scaling_choice: Callable[[float, float], float] = min if container._resize_mode == Constants.CONTAIN else max
        scaling_factor: int = scaling_choice(container_width / image_width, container_height / image_height)
        new_image_width: int = int(
            image_width * scaling_factor) if container._width == Constants.AUTO else container._width
        new_image_height: int = int(
            image_height * scaling_factor) if container._height == Constants.AUTO else container._height
        return 1 if new_image_width <= 0 else new_image_width, 1 if new_image_height <= 0 else new_image_height

    def __init__(
            self,
            master: Optional[Misc] = None,
            *,
            background: Optional[str] = Constants.TRANSPARENT,
            filter: ImageFilter = Constants.DISABLED,
            height: Optional[SizeDescription] = Constants.AUTO,
            image: Optional[PathDescription] = None,
            resizemode: ResizeMode = Constants.CONTAIN,
            width: Optional[SizeDescription] = Constants.AUTO,
            **options: Any) -> None:
        """
        Valid option names:
        activebackground, anchor, background, borderwidth, cursor, filter, height, highlightbackground,
        highlightcolor, highlightthickness, image, justify, padx, pady, relief, resizemode, state, width.
        """
        self.check_options(**options)
        super().__init__(master, background=background, **options)
        self._image_filter: ImageFilter = Constants.DISABLED
        self._height: SizeDescription = Constants.AUTO
        self._image: Optional[Image] = None
        self._image_path: Optional[PathDescription] = None
        self._last_image: Optional[Image] = None
        self._photo_image: Optional[PhotoImage] = None
        self._resize_mode: ResizeMode = Constants.CONTAIN
        self._scheduled_update: Optional[str] = None
        self._width: SizeDescription = Constants.AUTO
        self.configure(filter=filter, height=height, image=image, resizemode=resizemode, width=width)
        self.bind(sequence="<Configure>", func=self.schedule_update, add=True)

    def schedule_update(self, event: Optional[Event] = None, milliseconds: int = UPDATE_MILLISECONDS) -> None:
        if self._scheduled_update is not None:
            self.after_cancel(id=self._scheduled_update)
            self._scheduled_update = None
        resize_thread: Thread = Thread(target=self.resize_image, daemon=True)
        self._scheduled_update = self.after(ms=milliseconds, func=resize_thread.start)

    def resize_image(self) -> None:
        if self._image is not None:
            new_size: tuple[int, int] = self.calculate_size(self, image=self._image)
            processed_image: Image = self._image.resize(size=new_size)
            if self._image_filter != "disabled":
                container_width: int = self.winfo_width() if self._width == Constants.AUTO else self._width
                container_height: int = self.winfo_height() if self._height == Constants.AUTO else self._height
                if self._image_filter == "blurred":
                    container_size: int = max(container_width, container_height)
                    processed_image = ImageProcessor.blur_image(
                        image=processed_image,
                        container_size=container_size)
                elif self._image_filter == "circular":
                    container_size: int = min(container_width, container_height)
                    processed_image = ImageProcessor.make_image_circular(
                        image=processed_image,
                        container_size=container_size)
            self.update_image(image=processed_image)
        self._scheduled_update = None

    def update_image(self, image: Image) -> None:
        if self._last_image and image.size == self._last_image.size and image == self._last_image:
            return None
        self._last_image = image
        photo_image: PhotoImage = PhotoImage(image)
        Misc.configure(self, image=photo_image)
        self._photo_image = photo_image

    def configure(self, **options: Any) -> Any:
        self.check_options(**options)
        image_filter: Optional[ImageFilter] = options.pop("filter", None)
        height: Optional[SizeDescription] = options.pop("height", None)
        if height == Constants.AUTO:
            options["height"] = 1
        image_path: Optional[PathDescription] = options.pop("image", None)
        resize_mode: Optional[ResizeMode] = options.pop("resizemode", None)
        width: Optional[SizeDescription] = options.pop("width", None)
        if width == Constants.AUTO:
            options["width"] = 1
        result: Any = super().configure(**options)
        if image_filter is not None:
            self._image_filter = image_filter
        if height is not None:
            self._height = height
        if image_path == "":
            self._image = self._image_path = self._photo_image = None
        elif image_path is not None:
            with open_image(fp=image_path) as image:
                self._image = image.convert(mode="RGBA")
            self._image_path = image_path
            self.schedule_update(milliseconds=0)
        if resize_mode is not None:
            self._resize_mode = resize_mode
        if width is not None:
            self._width = width
        return result
    config = configure

    def cget(self, key: str) -> Any:
        self.check_options(key=None)
        options: dict[str, Any] = {
            "height": self._height,
            "image": self._image_path,
            "resizemode": self._resize_mode,
            "width": self._width}
        return options.get(key) if key in options else super().cget(key)
    __getitem__ = cget
