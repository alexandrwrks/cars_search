from typing import AsyncGenerator, Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import new_session
from app.schemas.filters import ParametersSchema
from app.services.auth_service import AuthService
from app.services.cars import CarsService
from app.services.user_service import UserService


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


async def get_auth_service(
        session: AsyncSession = Depends(get_async_session),
):
    return AuthService(session)

access_security = HTTPBearer(
    scheme_name="AccessToken"
)

refresh_security = HTTPBearer(
    scheme_name="RefreshToken"
)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(access_security),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.check_user(credentials.credentials)


async def get_user_service(
        session: AsyncSession = Depends(get_async_session)
):
    return UserService(session)

async def get_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(refresh_security),
):
    return credentials.credentials