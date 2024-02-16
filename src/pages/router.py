from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.auth.router import get_current_user
from src.recipe.router import get_all_recipes, get_specific_recipe

router = APIRouter(
    prefix="",
    tags=[""]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def get_base_page(request: Request, all_recipes=Depends(get_all_recipes)):
    current_user = await get_current_user(request)
    return templates.TemplateResponse("home.html", {"request": request, "recipes": all_recipes["recipes"],
                                                    "current_user": current_user})


@router.get("/search={recipe_name}")
def get_base_page(request: Request, specific_recipes=Depends(get_specific_recipe)):
    return templates.TemplateResponse("home.html", {"request": request, "recipes": specific_recipes["recipes"]})

#
# @router.get("/add_recipe")
# async def get_add_page(request: Request):
#     current_user = await get_current_user(request)
#     return templates.TemplateResponse("add_recipe.html", {"request": request, "current_user": current_user})
