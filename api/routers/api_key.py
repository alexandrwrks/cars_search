from fastapi import APIRouter, Depends, Query

from api.deps import get_api_service, get_current_user
from api.service.api_key_service import APIKeyService
from database.models import APIUsers

router =APIRouter(
    prefix="/api_key",
    tags=["api_key"],
)

@router.post("/")
async def create_api_key(
        name: str = Query(..., min_length=3),
        current_user: APIUsers = Depends(get_current_user),
        api_service: APIKeyService = Depends(get_api_service)
):
    return await api_service.create_api_key(current_user.id, name)