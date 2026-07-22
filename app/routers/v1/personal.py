from fastapi import APIRouter, Depends

from app.deps import get_current_user, get_user_service
from app.services.user_service import UserService
from database.models import Users

router = APIRouter()


@router.get("/info")
async def info(
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """Информация о пользователе"""
    return await user_service.get_user_by_id(current_user.id)


@router.get("/cards")
async def cards(
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """Объявления пользователя"""
    return await user_service.cards(current_user.id)

@router.get("/cards/{card_id}")
async def cards_by_id(
        card_id: int,
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """Выдача всей информации о машине по car_id"""
    return await user_service.get_cards_by_id(card_id)


@router.get("/favorites")
async def favorites(
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """Получение всех объявлений находящихся в избранном"""
    return await user_service.get_favorites(current_user.id)


@router.post("/favorites/{car_id}")
async def add_favorites(
        car_id: int,
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """Выдача всей информации о машине по car_id"""
    return await user_service.add_favorite_car(car_id, current_user.id)


@router.delete("/favorites/{car_id}")
async def remove_favorites(
        car_id: int,
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    """Удаление объявления из избранного"""
    return await user_service.delete_favorites(car_id, current_user.id)

