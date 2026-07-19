from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Links


class LinksRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_link(self, car_id: int, title: str):
        await self.session.execute(
            insert(Links)
            .values(car_id=car_id, title=title)
        )