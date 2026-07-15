import pytest


@pytest.mark.asyncio
async def test_get_car_by_id(client):
    car_id = 204954304
    response = await client.get(f"/v1/cars/{car_id}")

    assert response.status_code == 200

    data = response.json()

    assert "brand" in data
    assert "model" in data
    assert "year" in data