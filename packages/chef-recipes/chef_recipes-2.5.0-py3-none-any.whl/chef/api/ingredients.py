from typing import List

from fastapi import APIRouter

from chef.api.common import generic_get, generic_get_all, generic_delete, generic_update
from chef.controllers import IngredientsController
from chef.schemas import Ingredient, UpdateIngredient

router = APIRouter()
ingredients = IngredientsController()


@router.get("")
async def get_ingredients() -> List[Ingredient]:
    return await generic_get_all(ingredients)


@router.get("/{item_id}")
async def get_ingredient(item_id: int) -> Ingredient:
    return await generic_get(ingredients, item_id)


@router.delete("/{item_id}")
async def delete_ingredient(item_id: int) -> None:
    return await generic_delete(ingredients, item_id)


@router.put("/{item_id}")
async def update_ingredient(item_id, update_data: UpdateIngredient):
    return await generic_update(ingredients, item_id, update_data)
