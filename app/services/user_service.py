from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.user import UserRepo


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepo(session)

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def cards(self, user_id: int):
        # cards = await self.user_repo.get_user_cars(user_id)
        # if not cards:
        #     return []

        return []