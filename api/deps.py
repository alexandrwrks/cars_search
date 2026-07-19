from fastapi import Header, HTTPException, status, Request
from starlette.middleware.base import BaseHTTPMiddleware

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


class VerifyHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("X-Api-Key")

        if api_key != API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key"
            )

        return await call_next(request)