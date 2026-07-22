from typing import List

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Currency
from scripts.exchange_service.schemas import CurrencySchema


class ExchangeRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_currency_rate(self, data: List[CurrencySchema]):
        for currency in data:
            await self.session.execute(
                insert(Currency)
                .values(
                    base_currency=currency.base.value,
                    quote_currency=currency.quote.value,
                    rate=currency.rate,
                    rate_updated_at=currency.date,
                )
            )

    async def update_currency_rate(self, data: List[CurrencySchema]):
        for currency in data:
            await self.session.execute(
                update(Currency)
                .where(
                    Currency.base_currency == currency.base.value,
                    Currency.quote_currency == currency.quote.value
                )
                .values(
                    rate=currency.rate,
                    rate_updated_at=currency.date
                )
            )

    async def get_currency_rate(self) -> List[Currency]:
        result = await self.session.execute(
            select(Currency)
        )

        return result.scalars().all()