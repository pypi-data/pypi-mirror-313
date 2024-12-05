import asyncio
import glob
import os

from sqlalchemy.orm import Session

from chef.models import engine
from chef.settings import settings

from chef.controllers import RecipesController

recipes = RecipesController()


def __is_number(string: str):
    try:
        int(string.split("/")[-1])
        return True
    except:
        return False


def run():

    folders = glob.glob(settings.images_folder + "/*")
    recipe_folders = [f for f in folders if __is_number(f)]

    with Session(engine()) as db_session:
        for recipe_folder in recipe_folders:
            recipe_id = int(recipe_folder.split("/")[-1])
            image_path = os.path.join(recipe_folder, 'medium.jpeg')

            recipes.update_thumbnail(db_session, recipe_id, image_path)
            recipes.update_image(db_session, recipe_id, image_path)

        db_session.commit()


if __name__ == "__main__":
    run()
