import typing
from datetime import datetime
from typing import List, Generic, TypeVar, Union, Type, Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from chef.models import Category as CategoryDb, Recipe as RecipeDb
from chef.schemas import Recipe, Tag, Category, Ingredient, CreateOrUpdateRecipe, \
    IngredientItem, Unit, UpdateIngredient, CreateOrUpdateCategory

from chef.image.thumbnailer import compress_and_store
from chef.settings import settings

C = TypeVar('C', bound=BaseModel)
R = TypeVar('R', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)


class Controller(Generic[C, R, U]):

    @property
    def create_schema(self) -> Type[C]:
        return typing.get_args(self.__orig_bases__[0])[0]

    @property
    def read_schema(self) -> Type[R]:
        return typing.get_args(self.__orig_bases__[0])[1]

    @property
    def orm(self):
        return self.read_schema.Meta.orm_model

    @property
    def update_schema(self) -> Type[U]:
        return typing.get_args(self.__orig_bases__[0])[2]

    async def _fill_model(self, session: Session, model, data: Union[C, U]):
        """Override for more complex models."""
        for attr, value in data.dict(exclude_none=True).items():
            if attr in data.get_excluded_fields():
                continue
            setattr(model, attr, value)

    async def get_all(self, session: Session) -> List[R]:
        return [
            self.get_transform(self.read_schema(**item.dictionary))
            for item in session.scalars(select(self.read_schema.Meta.orm_model)).all()
        ]

    def get_transform(self, item: R) -> R:
        return item

    async def get_single_or_none(self, session: Session, item_id: int) -> Optional[R]:
        db_item = session.get(self.read_schema.Meta.orm_model, item_id)
        if db_item:
            return self.get_transform(self.read_schema(**db_item.dictionary))

        return None

    async def get_single(self, session: Session, item_id: int) -> R:
        recipe = await self.get_single_or_none(session, item_id)
        if not recipe:
            raise HTTPException(
                status_code=404, detail=f"{self.read_schema.__class__} id={item_id} not found"
            )
        return recipe

    async def delete_single(self, session: Session, item_id: int) -> None:
        item = session.get(self.read_schema.Meta.orm_model, item_id)
        if not item:
            raise HTTPException(
                status_code=404, detail=f"{self.read_schema.__class__} id={item_id} not found"
            )
        session.delete(item)
        session.commit()

    async def create(self, session: Session, data: C) -> R:
        new_model = self.read_schema.Meta.orm_model()
        await self._fill_model(session, new_model, data)
        session.add(new_model)
        session.commit()
        return await self.get_single(session, item_id=new_model.id)

    async def create_or_update(self, session: Session, data: Union[U, C]) -> R:
        if getattr(data, "id", None):
            item = session.get(self.read_schema.Meta.orm_model, data.id)
        else:
            item = self.read_schema.Meta.orm_model()
        await self._fill_model(session, item, data)
        session.add(item)
        session.commit()
        return self.read_schema(**session.get(self.read_schema.Meta.orm_model, item.id).dictionary)

    async def update(self, session: Session, item_id: int, data: U) -> R:
        item = session.get(self.read_schema.Meta.orm_model, item_id)
        if not item:
            raise HTTPException(
                status_code=404, detail=f"{self.read_schema.__class__} id={data.id} not found"
            )
        await self._fill_model(session, item, data)
        session.add(item)
        session.commit()
        return await self.get_single(session, item.id)


class TagController(Controller[Tag, Tag, Tag]):
    ...


class IngredientsController(Controller[UpdateIngredient, Ingredient, UpdateIngredient]):

    async def delete_single(self, session: Session, item_id: int) -> None:
        ingredient = session.get(self.read_schema.Meta.orm_model, item_id)
        if ingredient.ingredients_items:
            recipes = [
                r.title
                for item in ingredient.ingredients_items
                for r in item.recipes
            ]
            if recipes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ingredient still attached to some recipes: {', '.join(recipes)}",
                )
        return await super().delete_single(session, item_id)


class CategoriesController(Controller[CreateOrUpdateCategory, Category, CreateOrUpdateCategory]):

    async def _fill_model(self,  session: Session, model: CategoryDb, data: CreateOrUpdateCategory):
        tags = []
        for tag in data.tags:
            item = session.get(Tag.Meta.orm_model, tag.id)
            if not item:
                raise HTTPException(
                    status_code=400, detail=f"Tag id={tag.id} not found"
                )
            tags.append(item)
        for attr, value in data.dict(exclude_none=True, exclude={"tags": True}).items():
            setattr(model, attr, value)
        model.tags = tags


class UnitsController(Controller[Unit, Unit, Unit]):

    async def create_or_update(self, session: Session, data: Union[U, C]) -> R:
        if getattr(data, "id", None):
            item = session.get(self.read_schema.Meta.orm_model, data.id)
        else:
            same_name = session \
                .query(self.read_schema.Meta.orm_model) \
                .filter_by(name=data.name) \
                .first()
            if same_name:
                item = same_name
            else:
                item = self.read_schema.Meta.orm_model()
        for attr in data.dict(exclude={"id": True}):
            setattr(item, attr, getattr(data, attr))
        session.add(item)
        session.commit()
        return self.read_schema(
            **session.query(self.read_schema.Meta.orm_model)
            .filter_by(name=item.name)
            .first()
            .dictionary
        )


class RecipesController(Controller[CreateOrUpdateRecipe, Recipe, CreateOrUpdateRecipe]):

    def get_transform(self, item: Recipe) -> Recipe:
        if item.detail_image:
            item.detail_image = settings.public_url + item.detail_image

        if item.thumbnail_image:
            item.thumbnail_image = settings.public_url + item.thumbnail_image

        return item

    @staticmethod
    async def _get_ingredients_and_tags(session: Session, data: CreateOrUpdateRecipe):
        """Load (or create and load) entire models and for specified ingredients and tags."""
        updated_ingredients = []
        ingredients_controller = IngredientsController()
        units_controller = UnitsController()
        for ingredient_item in data.ingredients:
            updated_item = None
            if ingredient_item.id:
                updated_item = session.get(IngredientItem.Meta.orm_model, ingredient_item.id)
                for attr, value in ingredient_item.dict(
                        exclude_none=True,
                        exclude={"unit": True, "ingredient": True, 'id': True, 'uuid': True}
                ).items():
                    setattr(updated_item, attr, value)

            if not updated_item:
                updated_item = IngredientItem.Meta.orm_model(
                    **ingredient_item.dict(
                        exclude={'ingredient': True, 'unit': True, 'id': True, 'uuid': True}
                    )
                )
            u = await units_controller.create_or_update(session, ingredient_item.unit)
            updated_item.unit_id = u.id
            i = await ingredients_controller.create_or_update(session, ingredient_item.ingredient)
            updated_item.ingredient_id = i.id
            updated_ingredients.append(updated_item)

        updated_tags = []
        for tag in data.tags:
            if getattr(tag, "id", None):
                updated_tags.append(session.get(Tag.Meta.orm_model, tag.id))
            else:
                updated_tags.append(
                    Tag.Meta.orm_model(**tag.dict())
                )
        return updated_ingredients, updated_tags

    async def _fill_model(self, session: Session, model, data: Union[C, U]):
        if not model:
            raise HTTPException(
                status_code=404, detail=f"{self.read_schema.__class__} id={data.id} not found"
            )
        for attr, value in data.dict(
                exclude_none=True, exclude={"tags": True, "ingredients": True}
        ).items():
            setattr(model, attr, value)
        updated_ingredients, updated_tags = await self._get_ingredients_and_tags(session, data)
        model.ingredients = updated_ingredients
        model.tags = updated_tags

    async def get_by_category(self, session: Session, category_id: int = None) -> List[Recipe]:
        cat = session.scalars(
            select(Category.Meta.orm_model)
            .filter_by(id=category_id)
            .limit(1)
        ).first()
        if cat:
            result = [recipe for tag in cat.tags for recipe in tag.recipes]
            return [self.read_schema(**r.dictionary) for r in result]
        return []

    async def get_all_and_filter(self, session: Session, **filters: typing.Any) -> List[Recipe]:
        recipes = session.scalars(
            select(self.read_schema.Meta.orm_model)
            .filter_by(**filters)
        ).all()
        return [self.read_schema(**r.dictionary) for r in recipes]

    async def get_all_since(self, session: Session, since: datetime) -> List[Recipe]:
        recipes = session.scalars(
            select(self.read_schema.Meta.orm_model)
            .filter(RecipeDb.updated_at >= since)
        ).all()
        return [self.read_schema(**r.dictionary) for r in recipes]

    async def create_or_update(self, session: Session, data: Union[U, C]) -> R:
        raise ValueError("Not allowed on this controller!")

    def update_thumbnail(self, session: Session, recipe_id: int, image: any):
        url = compress_and_store(image, is_thumbnail=True)
        # recipe = (
        #     session
        #     .query(self.read_schema.Meta.orm_model)
        #     .filter_by(id=recipe_id)
        #     .first()
        # )
        # recipe.thumbnail_image = url
        # session.add(recipe)
        # try:
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        stmt = (
            update(self.read_schema.Meta.orm_model)
            .where(self.read_schema.Meta.orm_model.id == recipe_id)
            .values(thumbnail_image=url)
        )
        session.execute(statement=stmt)

    def update_image(self, session: Session, recipe_id: int, image: any):
        url = compress_and_store(image, is_thumbnail=False)
        # recipe = (
        #     session
        #     .query(self.read_schema.Meta.orm_model)
        #     .filter_by(id=recipe_id)
        #     .first()
        # )
        # recipe.detail_image = url
        # session.add(recipe)
        # try:
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        stmt = (
            update(self.read_schema.Meta.orm_model)
            .where(self.read_schema.Meta.orm_model.id == recipe_id)
            .values(detail_image=url)
        )
        session.execute(statement=stmt)
