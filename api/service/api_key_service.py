from sqlalchemy.ext.asyncio import AsyncSession

from api.repo.api_repo import APIRepo
from api.security import create_api_key


class APIKeyService:
    def __init__(self, session: AsyncSession):
        self.api_repo = APIRepo(session)

    async def create_api_key(self, user_id: int, name: str):
        api_key = create_api_key()

        await self.api_repo.create_api_key(user_id, api_key, name)

        return {
            "user_id": user_id,
            "api_key": api_key,
            "message": "API key created"
        }