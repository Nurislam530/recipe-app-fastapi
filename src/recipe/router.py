from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.recipe.schemas import RecipeCreate
from src.recipe.models import Recipe

router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"]
)


@router.get("/get_all_recipes")
async def get_all_recipes(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Recipe))
    recipes = result.scalars().all()
    return {"recipes": recipes}


@router.post("/add_recipe")
async def add_specific_recipe(new_recipe: RecipeCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Recipe).values(new_recipe.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "recipe successfully added into database"}


@router.get("/get_specific_recipe")
async def get_specific_recipe(recipe_name: str, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe).where(Recipe.name.icontains(f"%{recipe_name}%"))
    result = await session.execute(stmt)
    recipes = result.scalars().all()
    return {"recipes": recipes}
