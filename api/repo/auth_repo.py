from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.schema import AuthorizationSchema
from app.db.models import APIUsers


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

