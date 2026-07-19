import asyncio
from datetime import datetime

import httpx

from scripts.service.add_cars_service import car_service_add


async def get_new_cars():
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i in range(10):
            print(f"Машина №{i+1}")
            await car_service_add.save_parsed_car(client)

            print(f"Закончили в {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")

            await asyncio.sleep(30)