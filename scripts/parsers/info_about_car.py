import re
import json

import httpx
import pydantic

from bs4 import BeautifulSoup

from app.schemas.schemas import ParsedCar, CarInfo, CarImages


main_link = "https://kolesa.kz/a/show/"

def take_description(response: str) -> str | None:
    match = re.search(r'"descriptionText":"(.*?)","showTranslation"', response)

    if match:
        raw = match.group(1)

        # раскодируем \uXXXX и другие escape-последовательности
        try:
            raw = json.loads(f'"{raw}"')
        except json.JSONDecodeError:
            return None

        soup = BeautifulSoup(raw, "html.parser")

        description = soup.get_text()

        return description

    return None

async def parse_car(car_id: int, client: httpx.AsyncClient) -> ParsedCar | None:
    response = await client.get(f"{main_link}{car_id}")
    soup = BeautifulSoup(response.text, "html.parser")
    # if "Страница не найдена" or "Ссылка устарела или страницу удалили" in response.text:
    #     return None

    result = {}

    # ---------- Заголовок ----------
    title = soup.find("h1", class_="offer__title")

    if title:
        brand = title.find("span", itemprop="brand")
        model = title.find("span", itemprop="name")
        equipment = title.find("span", itemprop="equipment")
        year = title.find("span", class_="year")

        result["brand"] = brand.get_text(strip=True) if brand else None
        result["model"] = model.get_text(strip=True) if model else None
        result["generation"] = equipment.get_text(strip=True) if equipment else None
        result["year"] = int(year.get_text(strip=True)) if year else None

    # ---------- Цена ----------
    price = soup.find("div", class_="offer__price")

    if price:
        result["price"] = int(
            "".join(filter(str.isdigit, price.get_text()))
        )

    # ---------- Характеристики ----------
    params: dict[str, str] = {}

    for dl in soup.select("div.offer__parameters dl"):
        dt = dl.find("dt")
        dd = dl.find("dd")

        if not dt or not dd:
            continue

        key = dt.get_text(" ", strip=True)
        value = dd.get_text(" ", strip=True)

        params[key] = value

    location = params.get("Город")

    if location:
        parts = [part.strip() for part in location.split(",")]

        result["city"] = parts[0]
        result["region"] = parts[1] if len(parts) > 1 else None
    else:
        result["city"] = ""
        result["region"] = None

    result["generation"] = params.get("Поколение")
    result["body_type"] = params.get("Кузов")

    engine = params.get("Объем двигателя, л")

    if engine:
        match = re.match(r"([\d.]+)\s*\((.+)\)", engine)

        if match:
            result["engine_volume"] = float(match.group(1))
            result["fuel_type"] = match.group(2).replace(")", "").capitalize()

    result["transmission"] = params.get("Коробка передач")
    result["drive"] = params.get("Привод")
    result["steering"] = params.get("Руль")
    result["color"] = params.get("Цвет")

    result["customs_cleared"] = (
        params.get("Растаможен в Казахстане") == "Да"
    )

    # ---------- Описание ----------
    description = take_description(response.text)
    result["description"] = description
    # ---------- Фото ----------
    images = []
    result_images = {}
    for img in soup.select(".gallery__thumb button"):
        url = img.get("data-href")

        if url:
            images.append(url)

    result_images["images"] = images

    # ---------- Опции ----------
    options = []

    for option in soup.select(".offer__options li, .offer__options span"):
        text = option.get_text(strip=True)

        if text:
            options.append(text)

    result["options"] = options

    try:
        return ParsedCar(
            car_id=car_id,
            car=CarInfo(**result),
            images=CarImages(**result_images),
        )
    except pydantic.ValidationError:
        return None
