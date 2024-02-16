from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates

from src.auth.models import User
from src.auth.router import get_current_user
from src.database import get_async_session
from src.recipe.models import Recipe

router = APIRouter(
    prefix="/recipe",
    tags=["Recipe"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/get_all_recipes")
async def get_all_recipes(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Recipe))
    recipes = result.scalars().all()
    return {"recipes": recipes}


@router.get("/add")
async def get_add_recipe_page(request: Request):
    current_user = await get_current_user(request)
    return templates.TemplateResponse("add_recipe.html", {"request": request, "current_user": current_user})


@router.post("/add")
async def add_specific_recipe(request: Request, name: str = Form(...), ingredients: str = Form(...),
                              description: str = Form(...), session: AsyncSession = Depends(get_async_session)):
    current_user = await get_current_user(request)

    recipe_data = (
        insert(Recipe)
        .values(name=name,
                ingredients=ingredients,
                description=description,
                owner_id=current_user["id"]))
    await session.execute(recipe_data)
    await session.commit()

    return templates.TemplateResponse("add_recipe.html", {"request": request,
                                                          "current_user": current_user,
                                                          "msg": "recipe successfully added into database"
                                                          })


@router.get("/{recipe_id}")
async def get_specific_recipe(request: Request, recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe).where(Recipe.id == recipe_id)
    result = await session.execute(stmt)
    recipe = result.scalars().first()
    stmt2 = select(User).where(User.id == recipe.owner_id)
    result2 = await session.execute(stmt2)
    author = result2.scalars().first()
    return templates.TemplateResponse("recipe_page.html", {"request": request, "recipe": recipe, "author": author})
