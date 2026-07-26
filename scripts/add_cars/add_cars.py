import asyncio
from datetime import datetime

import httpx

from scripts.service.add_cars_service import car_service_add


async def get_new_cars():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"Старт: {datetime.now()}")
        for i in range(10):
            await car_service_add.save_parsed_car(client)

            await asyncio.sleep(30)
        print(f"Конец: {datetime.now()}")