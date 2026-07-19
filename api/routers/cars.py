from fastapi import APIRouter, Depends


from api.deps import check_api_key

from app.db.models import APIKeys

router = APIRouter(
    prefix="/openapi/v1/cars",
    tags=["cars"],
)


@router.get("/latest")
async def latest(
        api_key: APIKeys = Depends(check_api_key)
):
    return {"data": []}