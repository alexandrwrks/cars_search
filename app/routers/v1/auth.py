from fastapi import APIRouter, Depends, Query

from app.deps import get_auth_service
from app.schemas.response import ResponseUserSchema
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register", response_model=ResponseUserSchema)
async def register(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(username)


@router.post("/login", response_model=ResponseUserSchema)
async def login(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(username)


@router.post("/refresh")
async def refresh(
        refresh_token: str,
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh(refresh_token)


@router.post("/logout")
async def logout(
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.logout()