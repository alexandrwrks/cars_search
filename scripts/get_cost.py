import asyncio

import httpx

from app.repo.cars import CarsRepository
from app.schemas.filters import SortType
from database.config import new_session
from scripts.exchange_service.exchange_service import exchange_service

async def convert_kzt_to_usd():
    """
    Возращаем цену машины из KZT в USD

    :return: cost
    """
    async with new_session() as session:
        currency_data = await exchange_service.get_currency_rate()

        cars_repo = CarsRepository(session)
        cars = await cars_repo.get_cars(
            offset=0,
            sort=SortType.newest
        )

        for car in cars:
            for currency in currency_data:
                if car.currency == currency.quote.value:
                    print(
                        f"ID: {car.car_id}\n"
                        f"KZT to USD cost: {car.price / currency.rate:.2f}"
                    )

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.frankfurter.dev/v2/rates?from=2020-01-01&quotes=USD"
        )

        print(len(response.json()))
        print(response.json())


if __name__ == "__main__":
    asyncio.run(main())