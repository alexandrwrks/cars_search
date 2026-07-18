from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgre123@localhost:5432/test_cars"
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

test_session = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
    class_=AsyncSession
)