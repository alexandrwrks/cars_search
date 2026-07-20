from datetime import datetime, UTC, timedelta

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from api.schema import AuthorizationSchema
from database.models import APIUsers, APIRefreshTokens
from utils.settings import settings


class AuthRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, email: str) -> APIUsers | None:
        result = await self.session.execute(
            select(APIUsers)
            .where(APIUsers.email == email)
        )

        return result.scalar_one_or_none()

    async def create_user(self, data: AuthorizationSchema) -> int:
        result = await self.session.execute(
            insert(APIUsers)
            .values(
                email=data.email,
                password=data.password,
            )
            .returning(APIUsers.id)
        )

        return result.scalar_one()

    async def get_user_by_id(self, user_id: int) -> APIUsers | None:
        result = await self.session.execute(
            select(APIUsers)
            .where(APIUsers.id == user_id)
        )

        return result.scalar_one_or_none()

    async def delete_token(self, user_id: int, refresh_token: str) -> None:
        await self.session.execute(
            delete(APIRefreshTokens)
            .where(
                APIRefreshTokens.token == refresh_token,
                APIRefreshTokens.user_id == user_id
            )
        )

    async def insert_refresh_token(self, user_id: int, token: str) -> None:
        await self.session.execute(
            insert(APIRefreshTokens)
            .values(
                user_id=user_id,
                token=token,
                expired=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_DAYS)
            )
        )

    async def update_refresh_token(self, user_id: int, token: str) -> None:
        await self.session.execute(
            update(APIRefreshTokens)
            .where(APIRefreshTokens.user_id == user_id)
            .values(
                user_id=user_id,
                token=token,
                expired=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_DAYS)
            )
        )

    async def get_refresh_token(self, user_id: int) -> APIRefreshTokens | None:
        result = await self.session.execute(
            select(APIRefreshTokens)
            .where(APIRefreshTokens.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_token(self, refresh_token: str) -> APIRefreshTokens | None:
        result = await self.session.execute(
            select(APIRefreshTokens)
            .where(APIRefreshTokens.token == refresh_token)
        )
        return result.scalar_one_or_none()