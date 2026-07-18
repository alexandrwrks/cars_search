from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.cars import CarsRepository
from app.repo.favorite import FavoriteRepo
from app.repo.user import UserRepo


class UserService:
    """
    Сервис для работы с пользователями
    """
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepo(session)
        self.favorites_repo = FavoriteRepo(session)
        self.cars_repo = CarsRepository(session)

    async def get_user_by_id(self, user_id: int):

        user = await self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def cards(self, user_id: int):
        # cards = await self.user_repo.get_user_cars(user_id)
        # if not cards:
        #     return []

        return []

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
            raise HTTPException(status_code=404, detail="Car not found")

        return car

    async def get_favorites(self, user_id: int):
        cards = await self.favorites_repo.get_favorites(user_id)
        if not cards:
            return []

        return cards

    async def add_favorite_car(self, user_id: int, car_id: int):
        try:
            await self.favorites_repo.add_favorite(
                user_id, car_id
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add favorite car"
            )