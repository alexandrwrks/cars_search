import pytest


@pytest.mark.asyncio
async def test_get_cars(client):
    response = await client.get("/v1/cars/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data

    assert isinstance(data, dict)

