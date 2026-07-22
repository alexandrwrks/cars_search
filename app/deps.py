from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.filters import ParametersSchema
from app.services.auth_service import AuthService
from app.services.cars import CarsService
from app.services.user_service import UserService
from database.config import new_session
from services.cache.cache_service import CacheService
from services.cache.redis import redis


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        async with session.begin():
            yield session

async def get_redis() -> Redis:
    return redis


async def get_cache_service(
        redis: Redis = Depends(get_redis),
) -> CacheService:
    return CacheService(redis)

async def get_cars_service(
        session: AsyncSession = Depends(get_async_session),
        cache: CacheService = Depends(get_cache_service),
) -> CarsService:
    return CarsService(
        session=session,
        cache=cache
    )

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
        session: AsyncSession = Depends(get_async_session),
        cache: CacheService = Depends(get_cache_service)
):
    return UserService(session, cache)

async def get_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(refresh_security),
):
    return credentials.credentials