from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Users


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