from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Table, create_engine, \
    Engine, DateTime, func
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase, Mapped

from chef.settings import settings


def engine() -> Engine:
    return create_engine(settings.database_uri, echo=settings.log_sql)


def ensure_tables():
    Base.metadata.create_all(engine())


def _dictify(obj, depth=100):
    if obj is None:
        return None
    if issubclass(obj.__class__, Base) and depth > 0:
        return obj.get_dictionary(depth=depth - 1)
    if issubclass(obj.__class__, list):
        if depth > 1:
            return [_dictify(o, depth=depth - 1) for o in obj]
        else:
            return [str(o) for o in obj]
    if isinstance(obj, int) or isinstance(obj, float):
        return obj
    try:
        try:
            return int(obj)
        except (TypeError, ValueError):
            pass
        return float(obj)
    except (TypeError, ValueError, SyntaxError):
        pass
    return str(obj)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), server_onupdate=func.now())

    def _get_attributes(self, exclude: List[str] = None) -> dict:
        """Get model attributes to be parsed into JSON response"""
        if not exclude:
            exclude = []

        result = {}
        attributes = getattr(self, '__items__', [])
        for attr in attributes:
            if attr in exclude:
                continue
            try:
                result[attr] = getattr(self, attr)
            except AttributeError:
                continue
        return result

    def get_dictionary(self, depth=99, exclude=None):
        """Serialize recursively according to the __items__ attribute."""
        return {
            k: _dictify(v, depth=depth) for k, v in self._get_attributes(exclude=exclude).items()
        }

    @property
    def dictionary(self):
        return self.get_dictionary()


ingredients = Table(
    'ingredients',
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipe.id"), primary_key=True),
    Column("ingredient_item_id", Integer, ForeignKey("ingredient_item.id"), primary_key=True)
)

tags = Table(
    'tags',
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipe.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True)
)

category_tags = Table(
    'category_tags',
    Base.metadata,
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True)
)


class Unit(Base):
    __items__ = ["id", "name", "grams", "created_at", "updated_at"]
    __tablename__ = "unit"
    name = mapped_column(String(80), nullable=False, unique=True)
    grams = mapped_column(Float, default=0)


class Tag(Base):
    __items__ = ["id", "name", "created_at", "updated_at"]
    __tablename__ = "tag"
    name = mapped_column(String(80), nullable=False)
    categories: Mapped[List['Category']] = relationship(
        secondary=category_tags,
        back_populates="tags"
    )
    recipes: Mapped[List['Recipe']] = relationship(
        secondary=tags,
        back_populates="tags"
    )


class Ingredient(Base):
    __tablename__ = "ingredient"
    __items__ = [
        "id", "name", "energy", "fats",
        "carbs", "proteins", "fibres", "salt",
        "is_liquid", "density", "created_at", "updated_at"
    ]

    name = mapped_column(String(80), nullable=False)
    approx_per_piece = mapped_column(Float, default=0)  # g / piece

    energy = mapped_column(Float, default=0)  # kcal
    fats = mapped_column(Float, default=0)  # g / 100g
    carbs = mapped_column(Float, default=0)  # g / 100g
    proteins = mapped_column(Float, default=0)  # g / 100g
    fibres = mapped_column(Float, default=0)  # g / 100g
    salt = mapped_column(Float, default=0)  # g / 100g

    is_liquid = mapped_column(Boolean, default=False)
    density = mapped_column(Float, default=1000)  # g / L

    ingredients_items = relationship('IngredientItem', uselist=True, back_populates="ingredient")


class IngredientItem(Base):
    """
    -> [included in shopping list] <amount> <unit> <ingredient> (<note>)
    -> [x] 400 g tomatoes (roughly chopped)
    """
    __tablename__ = "ingredient_item"
    __items__ = ["id", "ingredient", "amount", "unit", "note", "order", "created_at", "updated_at"]

    ingredient_id = Column(Integer, ForeignKey(Ingredient.id))
    ingredient = relationship(Ingredient, uselist=False, back_populates="ingredients_items")
    amount = Column(Float, nullable=True, default=0)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=True)
    unit = relationship("Unit")
    order = Column(Integer, default=0)

    note = Column(String(10), nullable=True)
    exclude = Column(Boolean(), default=False)  # todo: remove?

    recipes = relationship('Recipe', secondary=ingredients, back_populates="ingredients")


class Category(Base):
    __tablename__ = "category"
    __items__ = ["id", "name", "tags", "created_at", "updated_at"]
    name = Column(String(80), nullable=False)
    tags: Mapped[List[Tag]] = relationship(
        secondary=category_tags,
        back_populates="categories"
    )


class Recipe(Base):
    __tablename__ = "recipe"
    __items__ = [
        "id",
        "title",
        "subtitle",
        "ingredients",
        "favorite",
        "body",
        "source",
        "source_name",
        "tags",
        "portions",
        "detail_image",
        "thumbnail_image",
        "created_at",
        "updated_at"
    ]

    title = Column(String(80), nullable=False)
    subtitle = Column(String(50), nullable=True)
    source_name = Column(String(100), nullable=True)
    source = Column(String(100), nullable=True)
    draft = Column(Boolean(), default=False)
    favorite = Column(Boolean(), default=False)
    portions = Column(Integer, default=4)
    thumbnail_image = Column(String(100), nullable=True)
    detail_image = Column(String(100), nullable=True)
    ingredients: Mapped[List[IngredientItem]] = relationship(
        secondary=ingredients,
        cascade="all",
        order_by="IngredientItem.order"
    )
    tags = relationship(
        Tag,
        secondary=tags,
        lazy="subquery",
        back_populates="recipes"
    )

    # HTML content + rich text editor on the frontend
    body = Column(String(1000), nullable=True)
