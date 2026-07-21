import pytest


@pytest.mark.asyncio
async def test_get_car_by_id(client):
    car_id = 214003611
    response = await client.get(url=f"/v1/cars/{car_id}")

    assert response.status_code == 200