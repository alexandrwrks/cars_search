from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import APIKeys


class APIRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_api_key(self, user_id: int, api_key: str, name: str) -> None:
        await self.session.execute(
            insert(APIKeys)
            .values(
                user_id=user_id,
                name=name,
                key_hash=api_key,
                plan_id=1,
            )
        )

    async def get_keys(self) -> List[APIKeys]:
        result = await self.session.execute(
            select(APIKeys)
        )

        return result.scalars().all()

    async def get_keys_by_key(self, key: str) -> APIKeys | None:
        result = await self.session.execute(
            select(APIKeys)
            .where(APIKeys.key_hash == key)
        )

        return result.scalar_one_or_none()