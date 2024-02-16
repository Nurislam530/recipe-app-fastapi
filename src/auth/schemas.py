from typing import Optional

from fastapi import Form
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseModel):
    email: str
    username: str
    role_id: int
    password: str

    @classmethod
    def as_form(
            cls,
            any_param: str = Form(...),
            any_other_param: int = Form(1)
    ):
        return cls(any_param=any_param, any_other_param=any_other_param)
