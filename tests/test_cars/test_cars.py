import pytest


@pytest.mark.asyncio
async def test_get_cars(client):
    response = await client.get("/v1/cars/")

    assert response.status_code == 200
    assert response.json() == {"total": 0, "items": []}