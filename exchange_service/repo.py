from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Currency


class ExchangeRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_currency(self, currency_data: dict):
        await self.session.execute(
            insert(Currency)
            .values(**currency_data)
        )