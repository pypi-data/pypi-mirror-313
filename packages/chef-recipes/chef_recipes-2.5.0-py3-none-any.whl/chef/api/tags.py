from typing import List

from fastapi import APIRouter

from chef.api.common import generic_get, generic_get_all, generic_delete, generic_create
from chef.controllers import TagController
from chef.schemas import Tag, UpdateTag

router = APIRouter()
tags = TagController()


@router.get("")
async def get_tags() -> List[Tag]:
    return await generic_get_all(tags)


@router.get("/{item_id}")
async def get_tag(item_id: int) -> Tag:
    return await generic_get(tags, item_id)


@router.post("", status_code=201)
async def create_tag(tag_data: UpdateTag) -> Tag:
    return await generic_create(tags, tag_data)


@router.delete("/{item_id}")
async def delete_tag(item_id: int) -> None:
    return await generic_delete(tags, item_id)
