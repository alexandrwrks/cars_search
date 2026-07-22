import json
from typing import Any, Type

from pydantic import BaseModel
from redis.asyncio import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str, schema: Type[BaseModel] | None = None, many: bool = False):
        value = await self.redis.get(key)

        if value is None:
            return None

        data = json.loads(value)

        if schema:
            if many:
                return [
                    schema.model_validate(item)
                    for item in data
                ]
            
            return schema.model_validate(data)

        return json.loads(value)

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600
    ):
        if isinstance(value, BaseModel):
            value = value.model_dump()

        elif isinstance(value, list):
            value = [
                item.model_dump() if isinstance(item, BaseModel) else item
                for item in value
            ]

        await self.redis.set(
            key,
            json.dumps(value),
            ex=expire
        )

    async def delete(self, key: str):
        await self.redis.delete(key)
