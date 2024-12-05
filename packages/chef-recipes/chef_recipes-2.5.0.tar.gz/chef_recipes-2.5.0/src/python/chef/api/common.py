from typing import TypeVar, List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from chef.controllers import Controller
from chef.models import engine

C = TypeVar('C', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)


async def generic_get(controller: Controller[C, R, U], item_id: int) -> R:
    with Session(engine()) as session:
        return await controller.get_single(session, item_id)


async def generic_get_all(controller: Controller[C, R, U]) -> List[R]:
    with Session(engine()) as session:
        return await controller.get_all(session)


async def generic_create(controller: Controller[C, R, U], create_data: C) -> R:
    with Session(engine()) as session:
        return await controller.create(session, create_data)


async def generic_delete(controller: Controller[C, R, U], item_id: int) -> None:
    with Session(engine()) as session:
        return await controller.delete_single(session, item_id)


async def generic_update(controller: Controller[C, R, U], item_id: int, data: U) -> R:
    with Session(engine()) as session:
        return await controller.update(session, item_id, data)
