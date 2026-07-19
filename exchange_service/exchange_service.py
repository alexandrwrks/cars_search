from sqlalchemy.ext.asyncio import AsyncSession

from exchange_service.repo import ExchangeRepo


class ExchangeService:
    def __init__(self, session: AsyncSession):
        self.exchange_repo = ExchangeRepo(session)

    # async def get_currency_rate(self, currency: dict):
    #     await
