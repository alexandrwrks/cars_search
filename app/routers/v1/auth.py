from fastapi import APIRouter, Depends, Query

from app.deps import get_auth_service, get_current_user, get_refresh_token
from app.schemas.response import ResponseUserSchema
from app.services.auth_service import AuthService
from database.models import Users

router = APIRouter()


@router.post("/register")
async def register(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service),
):
    """Регистрация нового пользователя"""
    return await auth_service.register(username)


@router.post("/login", response_model=ResponseUserSchema)
async def login(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service),
):
    """Авторизация пользователя"""
    return await auth_service.login(username)


@router.post("/refresh", response_model=ResponseUserSchema)
async def refresh(
        credentials = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
):
    """Обновление токенов"""
    return await auth_service.refresh(credentials)


@router.post("/logout")
async def logout(
        refresh_token: str,
        current_user: Users = Depends(get_current_user),
        auth_service: AuthService = Depends(get_auth_service),
):
    """Выход из системы с удалением refresh_token"""
    return await auth_service.logout(current_user.id, refresh_token)