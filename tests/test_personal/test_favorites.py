import pytest


@pytest.mark.asyncio
async def test_favorites(client):
    response = await client.post(
        "/v1/auth/login",
        params={
            "username": "Alex"
        }
    )

    assert response.status_code == 200
    access_token = response.json()["access_token"]
    print(access_token)

    response = await client.get(
        "/v1/personal/favorites",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    print(response.json())
