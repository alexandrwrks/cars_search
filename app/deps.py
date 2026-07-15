from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import new_session
from app.schemas.filters import ParametersSchema
from app.services.cars import CarsService


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        async with session.begin():
            yield session


async def get_cars_service(
        session: AsyncSession = Depends(get_async_session),
) -> CarsService:
    return CarsService(session)

def validate_parameters(
    params: ParametersSchema = Depends(),
) -> ParametersSchema:

    if (
        params.price_from is not None
        and params.price_to is not None
        and params.price_from > params.price_to
    ):
        raise HTTPException(
            status_code=422,
            detail="price_from не может быть больше price_to",
        )

    if (
        params.year_from is not None
        and params.year_to is not None
        and params.year_from > params.year_to
    ):
        raise HTTPException(
            status_code=422,
            detail="year_from не может быть больше year_to",
        )

    if (
        params.volume_from is not None
        and params.volume_to is not None
        and params.volume_from > params.volume_to
    ):
        raise HTTPException(
            status_code=422,
            detail="volume_from не может быть больше volume_to",
        )

    return params