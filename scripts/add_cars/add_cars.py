import asyncio
from datetime import datetime

import httpx

from scripts.service.add_cars_service import car_service_add


async def main():
    print(datetime.now().strftime("%d.%m.%Y %H:%M"))
    print("Начало парсинга...")
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            for i in range(10):
                print(f"Машина №{i+1}")
                await car_service_add.save_parsed_car(client)

                print(f"Закончили в {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")

                await asyncio.sleep(40)

            await asyncio.sleep(10 * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Конец парсинга...")