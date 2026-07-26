import httpx
from sqlalchemy.exc import IntegrityError

from app.repo.cars import CarsRepository
from database.config import new_session
from database.models import CurrencyType
from scripts.parsers.info_about_car import parse_car


class CarServiceAdd:
    async def save_parsed_car(self, client: httpx.AsyncClient):
        async with new_session() as session:
            async with session.begin():
                cars_repo = CarsRepository(session)
                car_id = await cars_repo.take_car_id()
                if car_id is None:
                    print("Нет ссылок для парсинга")
                    return

                try:
                    parsed_car = await parse_car(car_id, client)
                    if parsed_car is None:
                        await cars_repo.delete(car_id)
                        print(f"Машина удалена: {car_id}")
                        return

                    url = f"https://kolesa.kz/a/show/{parsed_car.car_id}"

                    await cars_repo.add_car_parameters(
                        car_id=car_id, url=url, car=parsed_car.car, currency=CurrencyType.KZT
                    )
                    print("Параметры машины успешно добавились")
                    if parsed_car.images.images:
                        values = [
                            {
                                "car_id": car_id,
                                "position": position,
                                "image_url": image_url
                            }
                            for position, image_url in enumerate(parsed_car.images.images, start=1)
                        ]
                        await cars_repo.add_car_image(values)
                    print("Успешно добавлены фотографии")
                    await cars_repo.change_parse(car_id)

                    print(
                        f"Успешное добавление машины\n"
                        f"CAR_ID: {car_id}\n"
                        f"Модель: {parsed_car.car.model}\n"
                    )

                except IntegrityError as e:
                    print(e)

                except (httpx.ReadTimeout, httpx.ReadError) as e:
                    print("Ошибка по httpx")

                except Exception as e:
                    print(e)

car_service_add = CarServiceAdd()