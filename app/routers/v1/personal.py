from fastapi import APIRouter, Depends

from database.models import Users
from app.deps import get_current_user, get_user_service
from app.services.user_service import UserService

router = APIRouter()


@router.get("/info")
async def info(
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_id(current_user.id)


@router.get("/cards")
async def cards(
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.cards(current_user.id)

@router.get("/cards/{card_id}")
async def cards_by_id(
        card_id: int,
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_cards_by_id(card_id)


@router.get("/favorites")
async def favorites(
        current_user: Users = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_favorites(current_user.id)