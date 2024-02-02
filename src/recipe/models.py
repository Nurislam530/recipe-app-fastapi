from typing import List

from sqlalchemy import Integer, String, Text, ForeignKey, ARRAY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.auth.models import User


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    ingredients: Mapped[str] = mapped_column(ARRAY(String), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id))


class Comment(Base):
    __tablename__ = "comment"

    id = mapped_column(Integer, primary_key=True)
    text = mapped_column(Text, nullable=True)
    rating = mapped_column(Integer, nullable=False)
    owner_id = mapped_column(Integer, ForeignKey(User.id))
    recipe_id = mapped_column(Integer, ForeignKey("recipe.id"))
