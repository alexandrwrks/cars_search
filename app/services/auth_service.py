from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.auth import AuthRepo
from app.schemas.response import ResponseUserSchema
from services.jwt_service import jwt_service
from utils.logger import logger


class AuthService:
    def __init__(self, session: AsyncSession):
        self.auth_repo = AuthRepo(session)

    async def register(self, username: str):
        """
        Регистрация пользователя

        :arg
            username : str

        :return
            dict

        :raise
            HTTPException
        """
        exists_user = await self.auth_repo.get_user(username)
        if exists_user is not None:
            logger.warning("Пользователь с таким username=%s уже существует", username)
            raise HTTPException(status_code=404, detail="User with this username already exists")

        user_id = await self.auth_repo.create_user(username)
        logger.info("Успешное создание нового аккаунта")
        return {
            "user_id": user_id,
            "username": username,
        }

    async def login(self, username: str) -> ResponseUserSchema:
        """
        Метод для авторизации пользователя на сайте
        Сохранение JWT refresh токена в БД

        :arg
            username : никнейм пользователя

        :returns
            ResponseUserSchema(
                access_token: str,
                refresh_token: str,
                token_type = "Bearer
            )


        :raise
            HTTPException
        """
        user = await self.auth_repo.get_user(username)
        if user is None:
            logger.warning("Ошибка авторизации. Пользователя с username=%s не существует", username)
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

    async def check_user(self, refresh_token: str):
        """
        Метод для проверки существования пользователя и проверки аутентификации

        :arg
            refresh_token : str

        :return
            exists_user: Users (database model)

        :raise
            HTTPException
        """
        payload = jwt_service.verify_access_token(refresh_token)
        user_id = int(payload['sub'])

        exists_user = await self.auth_repo.get_user_by_id(user_id)
        if exists_user is None:
            logger.warning("Пользователя с id=%s не существует", user_id)
            raise HTTPException(
                status_code=status.HTTP_404_BAD_REQUEST,
                detail="User does not exist"
            )

        return exists_user

    async def refresh(self, refresh_token: str) -> ResponseUserSchema:
        """
        Обновление access и refresh токенов

        :arg
            refresh_token : str

        :raise
            HTTPException
        """
        payload = jwt_service.verify_refresh_token(refresh_token)

        user_id = int(payload["sub"])

        token = await self.auth_repo.get_by_token(refresh_token)

        if token is None:
            logger.warning("Ошибка аутентификации пользователя")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User unregistered"
            )

        tokens = jwt_service.get_tokens(user_id)
        await self.auth_repo.update_refresh_token(user_id=user_id, token=tokens.refresh_token)
        return tokens

    async def logout(self, user_id: int, refresh_token: str):
        """
        Выход из приложения с удалением refresh_token

        :arg
            user_id: int

        :arg
            refresh_token: str

        :return
            dict

        :raise
            HTTPException
        """
        payload = jwt_service.verify_refresh_token(refresh_token)
        if payload['sub'] != user_id:
            logger.exception("Не валидный токен")
            raise HTTPException(status_code=404, detail="Not valid token for user")

        await self.auth_repo.delete_token(user_id, refresh_token)
        return {
            "message": "User logged out"
        }

