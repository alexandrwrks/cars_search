import pytest


# @pytest.mark.asyncio
# async def test_get_cars_with_params(client):
#
#     response = await client.get(
#         "/v1/cars/",
#         params={
#             "price_from": 5_000_000,
#             "price_to": 2_000_000,
#         }
#     )
#
#     assert response.status_code == 422
#     assert response.json() == {"detail": "price_from не может быть больше price_to"}