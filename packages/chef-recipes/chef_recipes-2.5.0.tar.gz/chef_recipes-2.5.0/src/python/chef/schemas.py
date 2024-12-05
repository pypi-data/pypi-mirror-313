from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, validator, Field, ConfigDict

from typing import List, Union, Optional

from chef.models import Recipe as RecipeDb
from chef.models import Category as CategoryDb
from chef.models import Tag as TagDb
from chef.models import IngredientItem as IngredientItemDb
from chef.models import Ingredient as IngredientDb
from chef.models import Unit as UnitDb


class Base(BaseModel):
    id: int

    class Meta:
        orm_model = None

    @staticmethod
    def get_excluded_fields():
        return []

class Named(Base):
    name: str


# ------- Unit ------- #

class Unit(Named):
    id: Union[int, None] = None
    grams: float = 0  # todo: how many grams in this unit - doesn't make sense

    class Meta:
        orm_model = UnitDb

# ------- Tag ------- #


class Tag(Named):

    class Meta:
        orm_model = TagDb


class UpdateTag(BaseModel):
    id: Union[int, None] = None
    name: str


# ------- Category ------- #

class Category(Named):
    tags: List[Tag] = Field(default_factory=list)

    class Meta:
        orm_model = CategoryDb


class CreateOrUpdateCategory(BaseModel):
    tags: List[Base] = Field(default_factory=list)
    name: str


# ------- Ingredient ------- #

class Ingredient(Named):
    approx_per_piece: float = 1  # g / piece

    energy: float = 0.0  # kcal
    fats: float = 0.0  # g / 100g
    carbs: float = 0.0  # g / 100g
    proteins: float = 0.0  # g / 100g
    fibres: float = 0.0  # g / 100g
    salt: float = 0.0  # g / 100g

    is_liquid: bool = False
    density: float = 1000.0  # g / L

    @staticmethod
    def get_excluded_fields():
        return ["uuid"]

    class Meta:
        orm_model = IngredientDb


class UpdateIngredient(Ingredient):
    """Update list of ingredients during a recipe create op...

    ...if 'id' is missing, new ingredient shall be created.
    """
    id: Union[int, None] = None


class IngredientItemBase(BaseModel):
    """
    -> [included in shopping list] <amount> <unit> <ingredient> (<note>)
    -> [x] 400 g tomatoes (roughly chopped)
    """
    ingredient: Ingredient
    amount: float
    unit: Unit
    order: Optional[int] = None
    uuid: UUID = Field(default_factory=uuid4)

    note: Union[str, None] = None
    exclude: bool = False  # todo: remove?


class IngredientItem(IngredientItemBase, Base):
    """
    -> [included in shopping list] <amount> <unit> <ingredient> (<note>)
    -> [x] 400 g tomatoes (roughly chopped)
    """
    class Meta:
        orm_model = IngredientItemDb
        exclude_items = ["uuid"]


class CreateOrUpdateIngredientItem(IngredientItemBase, BaseModel):
    id: Union[int, None] = None
    ingredient: UpdateIngredient
    unit: Unit = Unit(name="pcs")
    model_config = ConfigDict(extra='allow')


# ------- Recipe ------- #

class BaseRecipe(BaseModel):
    subtitle: Union[str, None] = None
    source_name: Union[str, None] = None
    source: Union[str, None] = None
    draft: bool = False
    favorite: bool = False
    portions: int = 4
    tags: List[Tag] = []


class RecipeDetail(BaseRecipe):
    subtitle: Union[str, None] = None
    source_name: Union[str, None] = None
    source: Union[str, None] = None
    draft: bool = False
    favorite: bool = False
    portions: int = 4
    ingredients: List[IngredientItem] = Field(default_factory=list)
    tags: List[Tag] = []

    # HTML content + rich text editor on the frontend
    body: Union[str, None] = None


class CreateOrUpdateRecipe(RecipeDetail, BaseModel):
    title: str  # mandatory
    ingredients: List[CreateOrUpdateIngredientItem] = Field(default_factory=list)
    tags: List[UpdateTag] = Field(default_factory=list)


class Recipe(Base, RecipeDetail):
    title: str
    thumbnail_image: Union[str, None]
    detail_image: Union[str, None]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Meta:
        orm_model = RecipeDb


class RecipeListItem(Base):
    title: str
    thumbnail_image: Union[str, None]
    detail_image: Union[str, None]
    tags: List[Tag] = []
