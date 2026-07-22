from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.repo.api_repo import APIRepo
from api.service.api_key_service import APIKeyService
from api.service.auth_service import AuthService
from app.deps import get_async_session


async def check_api_key(
    x_api_key: str = Header(alias="X-API-KEY"),
    session: AsyncSession = Depends(get_async_session),
):
    api_key = APIRepo(session)
    exists_keys = await api_key.get_keys_by_key(x_api_key)
    if exists_keys is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-API-KEY",
        )


async def verify_user_agent(
        user_agent: str = Header()
):
    if "MyApp" not in user_agent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid User Agent",
        )

access_security = HTTPBearer(
    scheme_name="AccessToken"
)

refresh_security = HTTPBearer(
    scheme_name="RefreshToken"
)

async def get_auth_service(
        session: AsyncSession = Depends(get_async_session),
):
    return AuthService(session)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(access_security),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.check_user(credentials.credentials)

async def get_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(refresh_security),
):
    return credentials.credentials

async def get_api_service(
        session: AsyncSession = Depends(get_async_session),
):
    return APIKeyService(session)