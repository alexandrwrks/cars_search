import asyncio

from database.models import Base
from tests.database import test_engine


async def create_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await test_engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_db())