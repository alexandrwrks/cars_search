import json
from typing import Any, Type

from pydantic import BaseModel
from redis.asyncio import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, schema: Type[BaseModel] | None = None):
        value = await self.redis.get(key)

        if value is None:
            return None

        data = json.loads(value)

        if schema:
            return schema.model_validate(data)

        return json.loads(value)

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600
    ):
        await self.redis.set(
            key,
            json.dumps(value),
            ex=expire
        )

    async def delete(self, key: str):
        await self.redis.delete(key)
