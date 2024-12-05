import os
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi import UploadFile
from loguru import logger

from chef.api.common import generic_get
from chef.controllers import RecipesController, CategoriesController
from chef.images import  CategoryHandler
from chef.settings import settings

recipes = RecipesController()
categories = CategoriesController()


router = APIRouter()


def _create_tmp_dir():
    upload_path = settings.upload_folder
    if not os.path.isdir(upload_path):
        raise HTTPException(status_code=500, detail="Server misconfiguration, invalid images path.")

    image_dir_name = f"chef_upload_{datetime.utcnow().timestamp()}"
    path = os.path.join(upload_path, image_dir_name)
    os.mkdir(path)
    return path


# @router.post('/recipes/{recipe_id}')
# async def post_recipe_image(recipe_id: int, image: UploadFile):
#     await generic_get(recipes, recipe_id)
#     logger.debug(f"uploading recipe (id={recipe_id}) image: {image.filename}, {image.size}b")
#
#     handler = Handler(image.file, recipe_id)
#     handler.create_images_set()
#
#     return f"Recipe images sent for processing...", 200
#
#
@router.post("/categories/{category_id}")
async def post_category_image(category_id, image: UploadFile):
    await generic_get(categories, category_id)

    logger.debug(f"uploading category (id={category_id}) image: {image.filename}, {image.size}b")
    handler = CategoryHandler(image.file, category_id)
    try:
        handler.create_images_set()
    except Exception as exc_info:
        logger.error("Image processing failed")
        logger.exception(exc_info)
        raise HTTPException(status_code=500, detail="Image processing failed") from exc_info

    return f"Images sent for processing...", 200
