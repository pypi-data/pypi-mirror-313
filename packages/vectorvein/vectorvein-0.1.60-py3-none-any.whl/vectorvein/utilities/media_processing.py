# @Author: Bi Ying
# @Date:   2024-07-27 12:03:49
import base64
from io import BytesIO
from pathlib import Path
from functools import cached_property

import httpx
from PIL import Image
from PIL.ImageFile import ImageFile


class ImageProcessor:
    def __init__(
        self,
        image_source: Image.Image | str | Path,
        max_size: int | None = 5 * 1024 * 1024,
        max_width: int | None = None,
        max_height: int | None = None,
    ):
        self.image_source = image_source
        if isinstance(image_source, (Image.Image, Path)):
            self.is_local = True
        else:
            self.is_local = not image_source.startswith("http")
        self.max_size = max_size
        self.max_width = max_width
        self.max_height = max_height
        self._image = self._load_image()
        self._image_format = self._image.format or "JPEG"
        self._cached_bytes = None
        self._cached_base64_image = None

    def _load_image(self):
        if not self.is_local and isinstance(self.image_source, str):
            image_url = self.image_source
            response = httpx.get(image_url)
            return Image.open(BytesIO(response.content))
        elif isinstance(self.image_source, (Path, str)):
            return Image.open(self.image_source)
        elif isinstance(self.image_source, Image.Image):
            return self.image_source
        else:
            raise ValueError(f"Unsupported image source type: {type(self.image_source)}")

    def _resize_image(
        self,
        img: ImageFile | Image.Image,
        max_size: int | None = None,
        max_width: int | None = None,
        max_height: int | None = None,
    ):
        img_bytes = BytesIO()
        image_format = img.format or "JPEG"
        _img = img.copy()
        _img.save(img_bytes, format=image_format, optimize=True)

        if max_width is not None and _img.width > max_width:
            new_size = (max_width, int(max_width * _img.height / _img.width))
            _img = _img.resize(new_size, Image.Resampling.LANCZOS)

        if max_height is not None and _img.height > max_height:
            new_size = (int(max_height * _img.width / _img.height), max_height)
            _img = _img.resize(new_size, Image.Resampling.LANCZOS)

        img_bytes = BytesIO()
        _img.save(img_bytes, format=image_format, optimize=True)

        if max_size is not None and img_bytes.getbuffer().nbytes <= max_size:
            return img_bytes

        original_size = _img.size
        scale_factor = 0.9

        while True:
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            img_resized = _img.resize(new_size, Image.Resampling.LANCZOS)

            img_bytes_resized = BytesIO()
            img_resized.save(img_bytes_resized, format=image_format, optimize=True)

            if max_size is not None and img_bytes_resized.getbuffer().nbytes <= max_size:
                return img_bytes_resized

            scale_factor -= 0.1
            if scale_factor < 0.1:
                return img_bytes_resized

    @property
    def bytes(self):
        if self._cached_bytes is not None:
            return self._cached_bytes
        if self.max_size is None and self.max_width is None and self.max_height is None:
            if isinstance(self._image, Image.Image):
                img_bytes = BytesIO()

                # 检查图像是否有透明通道
                has_transparency = self._image.mode in ("RGBA", "LA") or (
                    self._image.mode == "P" and "transparency" in self._image.info
                )

                if has_transparency:
                    # 如果有透明通道，使用PNG格式
                    save_format = "PNG"
                    self._image_format = "PNG"
                else:
                    # 如果没有透明通道，使用原始格式或默认为JPEG
                    save_format = self._image.format or self._image_format or "JPEG"

                    # 如果图像模式不是RGB（例如RGBA），转换为RGB
                    if self._image.mode != "RGB":
                        self._image = self._image.convert("RGB")

                self._image.save(img_bytes, format=save_format, optimize=True)
                self._cached_bytes = img_bytes.getvalue()
                return self._cached_bytes
            elif isinstance(self._image, BytesIO):
                self._cached_bytes = self._image.getvalue()
                return self._cached_bytes
            elif isinstance(self._image, ImageFile):
                if self._image.fp is None:
                    raise ValueError("Image file is not open")
                self._cached_bytes = self._image.fp.read()
                return self._cached_bytes

            self._cached_bytes = self._image.getvalue()
            return self._cached_bytes

        img_bytes_resized = self._resize_image(self._image, self.max_size, self.max_width, self.max_height)
        return img_bytes_resized.getvalue()

    @property
    def base64_image(self):
        if self.max_size is None and self.max_width is None and self.max_height is None:
            self._cached_base64_image = base64.b64encode(self.bytes).decode()
            return self._cached_base64_image

        img_bytes_resized = self._resize_image(self._image, self.max_size, self.max_width, self.max_height)
        self._cached_base64_image = base64.b64encode(img_bytes_resized.getvalue()).decode()
        return self._cached_base64_image

    @property
    def mime_type(self):
        return Image.MIME[self._image_format]

    @cached_property
    def data_url(self):
        return f"data:{self.mime_type};base64,{self.base64_image}"
