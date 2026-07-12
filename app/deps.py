from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import new_session
from app.services.cars import CarsService


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        async with session.begin():
            yield session


async def get_cars_service(
        session: AsyncSession = Depends(get_async_session),
) -> CarsService:
    return CarsService(session)