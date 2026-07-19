import asyncio
from typing import List

import httpx

from database.models import CurrencyType
from scripts.exchange_service.schemas import CurrencySchema
from utils.logger import logger


async def update_currency_rate() -> List[CurrencySchema] | None:
    try:
        async with httpx.AsyncClient() as client:
            need_currency = ",".join(currency.value for currency in CurrencyType)
            response = await client.get(
                url=f"https://api.frankfurter.dev/v2/rates?base=USD&quotes={need_currency}",
            )

        return [
            CurrencySchema(**currency)
            for currency in response.json()
        ]

    except httpx.HTTPError as e:
        print("Ошибка httpx", e)
        logger.exception("Ошибка получения валют с api")
        return None
