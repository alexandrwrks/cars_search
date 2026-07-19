import asyncio

import httpx

from database.models import CurrencyType

async def get_need_currency():
    async with httpx.AsyncClient() as client:
        need_currency = ",".join(currency.value for currency in CurrencyType)
        print(need_currency)
        response = await client.get(
            url=f"https://api.frankfurter.dev/v2/rates?base=USD&quotes={need_currency}",
        )

        print(response.json())

if __name__ == "__main__":
    asyncio.run(get_need_currency())