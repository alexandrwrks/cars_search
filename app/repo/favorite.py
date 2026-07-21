from typing import List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import Favorites, Cars


class FavoriteRepo:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_favorite(self, user_id: int, car_id: int):
        """
        Добавление объявление в избранные

        :arg
            user_id: int : ID пользователя
            car_id: int : ID машины/объявление
        """
        await self.session.execute(
            insert(Favorites)
            .values(
                user_id=user_id,
                car_id=car_id
            )
        )

    async def get_favorites(self, user_id: int):
        """
        Получаем все избранные пользователя

        :arg
            user_id: int : ID пользователя

        :returns
            Список всех избранных машин
        """
        result = await self.session.execute(
            select(Cars)
            .join(Favorites, Favorites.car_id == Cars.car_id)
            .where(
                Favorites.user_id == user_id,
                Cars.is_active.is_(True),
            )
            .order_by(Favorites.created_at.desc())
        )

        return result.scalars().all()

    async def delete_favorite(self, user_id: int, car_id: int):
        await self.session.execute(
            delete(Favorites)
            .where(
                Favorites.user_id == user_id,
                Favorites.car_id == car_id
            )
        )