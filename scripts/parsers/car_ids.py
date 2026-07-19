import asyncio
import random

import httpx

from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError

from app.repo.links import LinksRepo
from database.config import new_session
from app.extract import extract_car_id

url = "https://kolesa.kz/cars/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/137.0 Safari/537.36"
    )
}

async def main():
    count_of_cars = 0
    async with new_session() as session:
        links_repo = LinksRepo(session)

        async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
            for i in range(387, 1000):
                try:
                    response = await client.get(url, params={"page": i + 2})
                    response.raise_for_status()

                except httpx.ReadTimeout:
                    print(f"Таймаут на странице {i + 2}")
                    await asyncio.sleep(2)
                    continue

                except httpx.ConnectError:
                    print(f"Не удалось подключиться к странице {i + 2}")
                    await asyncio.sleep(5)
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                main_div = soup.find("div", class_="a-list")
                if main_div is None:
                    print("Не удалось найти список объявлений")
                    continue

                cars = main_div.find_all("div", class_="a-card__header")
                if not cars:
                    print("Объявления закончились.")
                    break

                count_of_cars += len(cars)
                print(f"Страница {i + 2}: найдено {len(cars)} объявлений")

                for car in cars:
                    a = car.find("a", class_="a-card__link")

                    link = a.get("href")
                    title = a.get_text(strip=True)

                    car_id = extract_car_id(link)

                    try:
                        await links_repo.add_link(car_id, title)
                    except IntegrityError as e:
                        print(e)
                        await session.rollback()
                await session.commit()
                print("Добавил 20 машин в БД")

                await asyncio.sleep(random.uniform(3, 10))


        print(f"\n\nВсего найденных машин:", count_of_cars)


if __name__ == "__main__":
    try:
        print("Начало парсинга...")
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(e)