from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.repo.auth_repo import AuthRepo
from api.schema import AuthorizationSchema
from services.jwt_service import jwt_service


class AuthService:
    def __init__(self, session: AsyncSession):
        self.auth_repo = AuthRepo(session)

    async def register(self, data: AuthorizationSchema):
        exists_user = await self.auth_repo.get_user(data.email)
        if exists_user is not None:
            raise HTTPException(status_code=404, detail="User with this username already exists")

        user_id = await self.auth_repo.create_user(data)
        return {
            "user_id": user_id,
            "email": data.email,
        }

    async def login(self, data: AuthorizationSchema):
        """
        Метод для авторизации пользователя на сайте
        Сохранение JWT refresh токена в БД

        :arg
            username : никнейм пользователя

        :returns
            ResponseUserSchema

        :raise
            HTTPException
        """
        user = await self.auth_repo.get_user(data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User unregistered"
            )

        tokens = jwt_service.get_tokens(user.id)
        exists_token = await self.auth_repo.get_refresh_token(user.id)
        if exists_token is None:
            await self.auth_repo.insert_refresh_token(user.id, tokens.refresh_token)
        await self.auth_repo.update_refresh_token(user.id, tokens.refresh_token)
        return tokens

    async def check_user(self, credentials: str):
        payload = jwt_service.verify_access_token(credentials)
        user_id = int(payload['sub'])

        exists_user = await self.auth_repo.get_user_by_id(user_id)
        if exists_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail="User does not exist"
            )

        return exists_user

    async def refresh(self, refresh_token: str):
        payload = jwt_service.verify_refresh_token(refresh_token)

        user_id = int(payload["sub"])

        token = await self.auth_repo.get_by_token(refresh_token)

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User unregistered"
            )

        tokens = jwt_service.get_tokens(user_id)
        await self.auth_repo.update_refresh_token(user_id=user_id, token=tokens.refresh_token)
        return tokens

    async def logout(self, refresh_token: str):
        payload = jwt_service.verify_refresh_token(refresh_token)
        if not payload['sub']:
            raise HTTPException(status_code=404, detail="Not valid token for user")

        await self.auth_repo.delete_token(int(payload["sub"]), refresh_token)
        return {
            "message": "User logged out"
        }

