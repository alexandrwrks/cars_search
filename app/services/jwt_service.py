from datetime import datetime, timedelta, UTC
from typing import Any

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status

from app.schemas.response import ResponseUserSchema
from utils.logger import logger
from utils.settings import settings


class JWTService:
    """
    Сервис для работы с JWT-токенами.

	Предоставляет методы для создания, проверки и декодирования
	access и refresh токенов.
    """
    ACCESS = "access"
    REFRESH = "refresh"

    def __init__(self):
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_MINUTES = settings.ACCESS_TOKEN_MINUTES
        self.REFRESH_TOKEN_DAYS = settings.REFRESH_TOKEN_DAYS
        self.SECRET_API_KEY = settings.SECRET_API_KEY


    def create_token(self, user_id: int, token_type: str, delta: timedelta) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "token_type": token_type,
            "exp": now + delta,
            "iat": now,
        }

        return jwt.encode(
            payload,
            self.SECRET_API_KEY,
            algorithm=self.ALGORITHM
        )

    def get_tokens(self, user_id: int) -> ResponseUserSchema:
        return ResponseUserSchema(
            access_token=self.create_access_token(user_id),
            refresh_token=self.create_refresh_token(user_id),
        )

    def create_access_token(self, user_id: int) -> str:
        return self.create_token(
            user_id=user_id,
            token_type=self.ACCESS,
            delta=timedelta(minutes=self.ACCESS_TOKEN_MINUTES)
        )

    def create_refresh_token(self, user_id: int) -> str:
        return self.create_token(
            user_id=user_id,
            token_type=self.REFRESH,
            delta=timedelta(days=self.REFRESH_TOKEN_DAYS)
        )

    def verify_token(self, credentials: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                credentials,
                self.SECRET_API_KEY,
                algorithms=[self.ALGORITHM]
            )
        except ExpiredSignatureError:
            logger.warning("Access token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        except InvalidTokenError:
            logger.warning("Invalid JWT token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    def verify_token_type(self, payload: dict[str, Any], token_type: str) -> dict[str, Any]:
        user_id = payload.get("sub")
        if user_id is None:
            logger.error("Invalid payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid payload",
            )
        if payload.get("token_type") != token_type:
            logger.error("Invalid token type")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload

    def verify_refresh_token(self, credentials: str) -> dict[str, Any]:
        payload = self.verify_token(credentials)
        return self.verify_token_type(payload, self.REFRESH)

    def verify_access_token(self, credentials: str) -> dict[str, Any]:
        payload = self.verify_token(credentials)
        return self.verify_token_type(payload, self.ACCESS)


jwt_service = JWTService()