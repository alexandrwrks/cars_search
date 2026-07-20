from fastapi import APIRouter, Depends

from api.deps import get_current_user, get_auth_service, get_refresh_token
from api.schema import AuthorizationSchema
from api.service.auth_service import AuthService
from database.models import APIUsers

router = APIRouter(
    prefix="/openapi/v1/auth",
    tags=["auth"],
)

@router.post("/register")
async def register(
        data: AuthorizationSchema,
        auth_service: AuthService = Depends(),
):
    return await auth_service.register(data)

@router.post("/login")
async def login(
        data: AuthorizationSchema,
        auth_service: AuthService = Depends(),
):
    return await auth_service.login(data)

@router.post("/logout")
async def refresh(
        credentials = Depends(get_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh(credentials)

@router.post("/logout")
async def logout(
        refresh_token: str,
        current_user: APIUsers = Depends(get_current_user),
        auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.logout(current_user.id, refresh_token)