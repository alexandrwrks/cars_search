from fastapi import APIRouter, Depends, Query

from api.deps import check_api_key
from app.deps import get_cars_service, validate_parameters
from app.schemas.filters import ParametersSchema
from app.services.cars import CarsService
from database.models import APIKeys

router = APIRouter(
    prefix="/openapi/v1/cars",
    tags=["cars"],
)


@router.get("/")
async def latest(
        page: int = Query(0),
        params: ParametersSchema = Depends(validate_parameters),
        api_key: APIKeys = Depends(check_api_key),
        cars_service: CarsService = Depends(get_cars_service),
):
    return await cars_service.get_cars_with_params_type(page, params)
