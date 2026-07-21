import asyncio
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.cars import CarsRepository
from app.repo.favorite import FavoriteRepo
from app.repo.user import UserRepo
from app.schemas.filters import CarResponse
from services.cache.cache_service import CacheService
from utils.logger import logger


class UserService:
    """
    Сервис для работы с пользователями
    """

    def __init__(self, session: AsyncSession, cache: CacheService):
        self.user_repo = UserRepo(session)
        self.favorites_repo = FavoriteRepo(session)
        self.cars_repo = CarsRepository(session)
        self.cache = cache

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None:
            logger.warning("Пользователь id=%s не существует", user_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    async def cards(self, user_id: int):
        # cards = await self.user_repo.get_user_cars(user_id)
        # if not cards:
        #     return []

        return {
            "message": "Находится в разработке"
        }

    async def get_cards_by_id(self, car_id: int):
        """
        Получить объявление созданные пользователем

        :arg
            card_id: int : ID пользователя

        :returns
            Объявление пользователя
        """
        car = await self.cars_repo.get_car_by_id(car_id)
        if car is None:
            logger.warning("Машина id=%s не найдена", car_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
            )

        return car

    async def get_favorites(self, user_id: int) -> List[CarResponse]:
        """
        Получение всех избранных объявлений пользователя

        :arg
            user_id: int

        :return
            List[CarResponse]
        """
        key = f"favorites:{user_id}"

        cached = await self.cache.get(key)
        if cached:
            return cached

        cars = await self.favorites_repo.get_favorites(user_id)
        if not cars:
            return []

        response = [
            CarResponse.model_validate(car).model_dump(mode="json")
            for car in cars
        ]

        await self.cache.set(key, response, expire=3600)

        return response

    async def add_favorite_car(self, car_id: int, user_id: int) -> dict:
        """
        Добавление машины с избранное

        :arg
            car_id: int

        :arg
            user_id: int

        :return
            dict

        :raise
            HTTPException
        """
        favorites = await self.favorites_repo.get_favorites(user_id)
        cars = await self.cars_repo.get_car_by_id(car_id)

        if cars is None:
            logger.error("Машины id=%s отсутствует", car_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Car not exists"
            )

        for fav in favorites:
            if fav.car_id == car_id:
                logger.warning("Ошибка добавление машины в избранное. Машина id=%s уже находится в избранном", car_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Car already add"
                )

        await asyncio.gather(
            self.favorites_repo.add_favorite(user_id, car_id),
            self.cache.delete(f"favorites:{user_id}")
        )
        return {"message": "Успешно добавлено в избранное"}

    async def delete_favorites(self, car_id: int, user_id: int) -> dict:
        """

        :arg
            car_id: int

        :arg
            user_id: int

        :return
            dict

        :raise
            HTTPException
        """
        favorites = await self.favorites_repo.get_favorites(user_id)
        for fav in favorites:
            if fav.car_id == car_id:
                await asyncio.gather(
                    self.favorites_repo.delete_favorite(user_id, car_id),
                    self.cache.delete(f"favorites:{user_id}")
                )
                return {"message": "Удаление объявления из избранного"}

        logger.error("Не удалось удалить машину id=%s из избранного", car_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
