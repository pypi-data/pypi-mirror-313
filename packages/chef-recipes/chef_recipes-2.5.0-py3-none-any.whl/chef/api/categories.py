from typing import List

from fastapi import APIRouter

from chef.api.common import generic_get, generic_get_all, generic_delete, generic_update, \
    generic_create
from chef.controllers import CategoriesController
from chef.schemas import Category, CreateOrUpdateCategory

router = APIRouter()
categories = CategoriesController()


@router.get("")
async def get_categories() -> List[Category]:
    return await generic_get_all(categories)


@router.post("", status_code=201)
async def create_category(create_data: CreateOrUpdateCategory) -> Category:
    return await generic_create(categories, create_data)


@router.get("/{item_id}")
async def get_category(item_id: int) -> Category:
    return await generic_get(categories, item_id)


@router.delete("/{item_id}")
async def delete_category(item_id: int) -> None:
    return await generic_delete(categories, item_id)


@router.put('/{item_id}')
async def update_category(item_id: int, update_data: CreateOrUpdateCategory) -> Category:
    return await generic_update(categories, item_id, update_data)
