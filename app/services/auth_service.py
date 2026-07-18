from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.auth import AuthRepo
from app.schemas.response import ResponseUserSchema
from app.services.jwt_service import jwt_service


class AuthService:
    def __init__(self, session: AsyncSession):
        self.auth_repo = AuthRepo(session)

    async def register(self, username: str) -> ResponseUserSchema:
        exists_user = await self.auth_repo.get_user(username)
        if exists_user is not None:
            raise HTTPException(status_code=404, detail="User with this username already exists")

        user_id = await self.auth_repo.create_user(username)
        return jwt_service.get_tokens(user_id)


    async def login(self, username: str) -> ResponseUserSchema:
        user = await self.auth_repo.get_user(username)
        if user is None:
            raise HTTPException(status_code=400, detail="User unregistered")

        return jwt_service.get_tokens(user.id)

    async def check_user(self, credentials: str):
        payload = jwt_service.verify_token(credentials)
        user_id = int(payload['sub'])

        exists_user = await self.auth_repo.get_user_by_id(user_id)
        if exists_user is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        return exists_user

    async def refresh(self, refresh_token: str):
        payload = jwt_service.verify_token(refresh_token)