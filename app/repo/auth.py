from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import RefreshTokens, Users
from utils.settings import settings


class AuthRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, username: str) -> Users | None:
        result = await self.session.execute(
            select(Users)
            .where(Users.username == username)
        )

        return result.scalar_one_or_none()

    async def create_user(self, username: str) -> int:
        result = await self.session.execute(
            insert(Users)
            .values(username=username)
            .returning(Users.id)
        )

        return result.scalar_one()

    async def get_user_by_id(self, user_id: int) -> Users | None:
        result = await self.session.execute(
            select(Users)
            .where(Users.id == user_id)
        )

        return result.scalar_one_or_none()

    async def delete_token(self, user_id: int, refresh_token: str) -> None:
        await self.session.execute(
            delete(RefreshTokens)
            .where(
                RefreshTokens.token == refresh_token,
                RefreshTokens.user_id == user_id
            )
        )

    async def insert_refresh_token(self, user_id: int, token: str) -> None:
        """
        Добавление нового refresh_token
        """
        await self.session.execute(
            insert(RefreshTokens)
            .values(
                user_id=user_id,
                token=token,
                expired=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_DAYS)
            )
        )

    async def update_refresh_token(self, user_id: int, token: str) -> None:
        await self.session.execute(
            update(RefreshTokens)
            .where(RefreshTokens.user_id == user_id)
            .values(
                user_id=user_id,
                token=token,
                expired=datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_DAYS)
            )
        )

    async def get_refresh_token(self, user_id: int) -> RefreshTokens | None:
        result = await self.session.execute(
            select(RefreshTokens)
            .where(RefreshTokens.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_token(self, refresh_token: str) -> RefreshTokens | None:
        result = await self.session.execute(
            select(RefreshTokens)
            .where(RefreshTokens.token == refresh_token)
        )
        return result.scalar_one_or_none()