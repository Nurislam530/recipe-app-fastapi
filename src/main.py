from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware

from src.database import User
from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.recipe.router import router as router_recipe
from src.auth.router import router as router_user
from src.pages.router import router as router_base

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "src/static"),
    name="static",
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_recipe)
app.include_router(router_user)
app.include_router(router_base)
