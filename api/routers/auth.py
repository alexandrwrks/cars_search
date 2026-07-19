from fastapi import APIRouter, Depends

from api.schema import AuthorizationSchema
from api.service.auth_service import AuthService

router = APIRouter(
    prefix="/openapi/v1/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
        data: AuthorizationSchema,
        auth_service: AuthService = Depends(),
):
    return await auth_service.login(data)