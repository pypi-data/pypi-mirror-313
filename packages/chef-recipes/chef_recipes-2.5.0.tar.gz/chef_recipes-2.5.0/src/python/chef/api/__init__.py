from fastapi import APIRouter

from chef.api.categories import router as category_router
from chef.api.ingredients import router as ingredient_router
from chef.api.recipes import router as recipe_router
from chef.api.tags import router as tag_router
from chef.api.images import router as image_router
from chef.api.units import router as units_router

api_router = APIRouter(prefix='/api')
api_router.include_router(recipe_router, prefix="/recipes")
api_router.include_router(category_router, prefix="/categories")
api_router.include_router(ingredient_router, prefix="/ingredients")
api_router.include_router(tag_router, prefix="/tags")
api_router.include_router(units_router, prefix="/units")
api_router.include_router(image_router, prefix="/images")
