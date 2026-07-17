from datetime import datetime, timedelta, UTC

import jwt
from fastapi import HTTPException, status


class JWTService:
    def __init__(self):
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_MINUTES = 30
        self.REFRESH_TOKEN_DAYS = 30
        self.SECRET_API_KEY = "67993c17230db7155fde061a98a444441bfa92d1e0f2c5863a70731b768dc9d2"

    async def create_token(self, user_id: int) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "exp": now + timedelta(minutes=self.ACCESS_TOKEN_MINUTES),
            "iat": now,
        }

        return jwt.encode(
            payload,
            self.SECRET_API_KEY,
            algorithm=self.ALGORITHM
        )

    async def verify_token(self, credentials: str) -> dict:
        try:
            return jwt.decode(
                credentials,
                self.SECRET_API_KEY,
                algorithms=[self.ALGORITHM]
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not valid token",
            )



jwt_service = JWTService()