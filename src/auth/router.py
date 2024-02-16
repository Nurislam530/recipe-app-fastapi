from datetime import timedelta, datetime
from typing import Optional, Annotated

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from src.auth.models import User

from src.database import get_async_session

router = APIRouter(
    prefix="/auth",
    tags=["User"]
)

templates = Jinja2Templates(directory="src/templates")

SECRET_KEY = "32kjg754toiejf09sdf892o3th6jlewfiud0s8e5j23io5h2"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str, session):
    stmt = select(User).where(User.username == username)
    existing_user = await session.execute(stmt)
    res = existing_user.scalars().first()

    print(username, password, res)

    if not res:
        return False
    if not verify_password(password, res.password):
        return False
    return res


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        return templates.TemplateResponse("login.html", {"request": request})


@router.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
def get_login_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/token")
async def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        return False
    token_expires = timedelta(minutes=30)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)

    return True


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.post("/register")
async def register_user(request: Request, email: str = Form(...), username: str = Form(...),
                        password1: str = Form(...), password2: str = Form(...),
                        session: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.email == email)
    existing_user = await session.execute(stmt)
    res = existing_user.scalars().all()

    if res:
        raise HTTPException(status_code=400, detail="Email already registered")

    if password1 != password2:
        msg = "Invalid registration request"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    hash_password = get_password_hash(password1)
    default_role_id = 1

    userdata = (
        insert(User)
        .values(email=email,
                username=username,
                password=hash_password,
                role_id=default_role_id))
    await session.execute(userdata)
    await session.commit()

    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: AsyncSession = Depends(get_async_session)):
    try:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form_data, session=session)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
