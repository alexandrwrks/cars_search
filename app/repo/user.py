from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Users, Cars


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> Users | None:
        result = await self.session.execute(
            select(Users).where(Users.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_user_cars(self, user_id: int) -> List[Cars]:
        result = await self.session.execute(
            select(Cars, func.count(Cars.id).label("count"))
            .join(Users, Cars.user_id == Users.id)
            .where(
                Users.id == user_id,
                Cars.is_active == True,
            )
        )

        return result.scalars()

    async def get_user_cars_by_user_id(self, user_id: int) -> List[Cars]:
        result = await self.session.execute(
            select(Cars).where(Cars.id == user_id)
        )

        return result.scalars().all()
