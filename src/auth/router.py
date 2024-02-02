from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User

from src.database import get_async_session


router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.get("/")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

