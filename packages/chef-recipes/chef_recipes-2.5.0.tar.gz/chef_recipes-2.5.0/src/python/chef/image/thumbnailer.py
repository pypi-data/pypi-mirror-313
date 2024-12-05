import os.path

import pillow_avif
from PIL import Image
from loguru import logger

from chef.image.storage import StorageProtocol, LocalStorage
from chef.settings import StorageType, ImageFormat

StorageBackends: dict[StorageType, StorageProtocol] = {
    StorageType.LOCAL: LocalStorage(),
    # implement more...
}


SIZES = {
    "thumbnail": (250, 250),
    "small": (476, 476),
    # "medium": (768, 768),
}


def _compress_and_store_avif(
        fp: any,
        image_format: ImageFormat,
        image_size: tuple[int, int],
        storage_backend: StorageType = StorageType.LOCAL
) -> str:
    image = Image.open(fp)
    image.thumbnail(image_size)
    logger.debug(f"Image shrunk to {image_size}")
    image_url = StorageBackends.get(storage_backend).store(image, image_format)
    logger.debug(f"Image stored ({storage_backend}) at: {image_url}")
    public_url = os.path.join("/images", image_url.split("/")[-1])
    logger.debug(f"Image available at: {public_url}")
    return public_url


def compress_and_store(
        fp: any,
        image_format: ImageFormat = ImageFormat.AVIF,
        is_thumbnail: bool = False,
) -> str:
    target_size = SIZES.get("thumbnail" if is_thumbnail else "small")

    if image_format == ImageFormat.AVIF:
        return _compress_and_store_avif(fp, ImageFormat.AVIF, target_size)

    msg = f"Unsupported image format: {image_format}"
    logger.error(msg)
    raise Exception(msg)
