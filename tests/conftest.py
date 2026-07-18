import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.deps import get_async_session
from app.main import app
from tests.database import test_session


@pytest_asyncio.fixture
async def session():
    async with test_session() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture
async def client(session):

    async def override_get_session():
        yield session

    app.dependency_overrides[get_async_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()