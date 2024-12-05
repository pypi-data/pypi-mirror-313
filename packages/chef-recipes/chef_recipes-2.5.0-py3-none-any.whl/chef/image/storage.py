from pathlib import Path
from typing import Protocol

from uuid import uuid4

from PIL.Image import Image

from chef.settings import settings, ImageFormat


class StorageProtocol(Protocol):

    def store(self, image: Image, image_format: ImageFormat) -> str:
        ...


class LocalStorage:

    system_path: Path
    image_quality: int

    def __init__(self, system_path: Path = None, image_quality: int = None):
        self.system_path = system_path or Path(settings.images_folder)
        self.image_quality = image_quality or 70

    def store(self, image: Image, image_format: ImageFormat) -> str:
        final_path = self.system_path / f"{uuid4()}.{image_format.lower()}"
        image.save(final_path, quality=self.image_quality, save_all=True)
        return str(final_path)
