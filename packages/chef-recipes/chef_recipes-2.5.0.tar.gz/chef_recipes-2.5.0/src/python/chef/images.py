import os

from PIL import Image
from chef.settings import settings

from loguru import logger


class Handler:

    THUMB = 96, 96
    SMALL = 540, 540
    MEDIUM = 768, 768
    LANDSCAPE = 1280, 720

    ALL_SIZES = [
        ("thumb", THUMB),
        ("small", SMALL),
        ("medium", MEDIUM)
    ]

    def __init__(self, file, item_id) -> None:
        self.file = file
        self.item_id = item_id
        self.target = settings.images_folder

    def _create_folder(self):
        if not os.path.isdir(self.target):
            os.makedirs(self.target, exist_ok=True)

        recipe_folder = os.path.join(self.target, str(self.item_id))
        if not os.path.isdir(recipe_folder):
            os.mkdir(recipe_folder)

        return recipe_folder

    def _sizes(self):
        return self.ALL_SIZES

    def create_images_set(self):
        image = Image.open(self.file)
        target_dir = self._create_folder()

        for name, size in self._sizes():
            tmp_img = image.copy()
            tmp_img.thumbnail(size, Image.LANCZOS)
            path = os.path.join(target_dir, f"{name}.jpeg")
            logger.info(f"Saving image to '{path}'")
            tmp_img.save(path)


class CategoryHandler(Handler):

    def _create_folder(self):
        if not os.path.isdir(self.target):
            logger.error(f"Images base DIR does not exist: {self.target}")
            raise Exception(f"Images base DIR does not exist: {self.target}")

        categories_folder = os.path.join(self.target, "categories")
        if not os.path.isdir(categories_folder):
            os.mkdir(categories_folder)

        category_folder = os.path.join(categories_folder, str(self.item_id))
        if not os.path.isdir(category_folder):
            os.mkdir(category_folder)

        return category_folder

    def _sizes(self):
        return [
            ("landscape", self.LANDSCAPE)
        ]
