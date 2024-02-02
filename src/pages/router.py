from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.recipe.router import get_all_recipes, get_specific_recipe

router = APIRouter(
    prefix="",
    tags=[""]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
def get_base_page(request: Request, all_recipes=Depends(get_all_recipes)):
    return templates.TemplateResponse("home.html", {"request": request, "recipes": all_recipes["recipes"]})


@router.get("/search={recipe_name}")
def get_base_page(request: Request, specific_recipes=Depends(get_specific_recipe)):
    return templates.TemplateResponse("home.html", {"request": request, "recipes": specific_recipes["recipes"]})


@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
def get_login_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
