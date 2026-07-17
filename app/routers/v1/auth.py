from fastapi import APIRouter, Depends, Query

from app.deps import get_auth_service
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(username)


@router.post("/login")
async def login(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(username)