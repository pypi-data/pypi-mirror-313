from typing import List

from fastapi import APIRouter

from chef.api.common import generic_get_all
from chef.controllers import UnitsController
from chef.schemas import Unit

router = APIRouter()
units = UnitsController()


@router.get("")
async def get_units() -> List[Unit]:
    return await generic_get_all(units)
