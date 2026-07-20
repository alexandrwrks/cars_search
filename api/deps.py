from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.service.auth_service import AuthService
from app.deps import get_async_session

API_KEY = "my_secret_key"


async def check_api_key(
    x_api_key: str = Header(alias="X-API-KEY"),
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
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