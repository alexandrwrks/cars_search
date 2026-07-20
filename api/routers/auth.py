from fastapi import APIRouter, Depends

from api.deps import get_auth_service, get_refresh_token
from api.schema import AuthorizationSchema
from api.service.auth_service import AuthService

router = APIRouter(
    prefix="/openapi/v1/auth",
    tags=["auth"],
)

@router.post("/register")
async def register(
        data: AuthorizationSchema = Depends(),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(data)

@router.post("/login")
async def login(
        data: AuthorizationSchema = Depends(),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(data)

@router.post("/refresh")
async def refresh(
        credentials = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh(credentials)

@router.post("/logout")
async def logout(
        credentials = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.logout(credentials)