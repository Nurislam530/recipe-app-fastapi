# from fastapi_users import FastAPIUsers
#
# from src.auth.auth import auth_backend
# from src.auth.manager import get_user_manager
# from src.auth.schemas import UserRead, UserCreate
# from src.database import User
#
# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )
#
# router = fastapi_users.get_register_router(UserRead, UserCreate)
#
#
# @router.post("/register")
# async def register_user(new_user: UserCreate):
#     return
