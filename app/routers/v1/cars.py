from fastapi import APIRouter, Depends, Query

from app.deps import get_cars_service, validate_parameters, get_current_user
from app.schemas.filters import ResponseParametersSchema, ParametersSchema, ResponseCarsType
from app.services.cars import CarsService
from database.models import Users

router = APIRouter()


@router.get("/", response_model=ResponseParametersSchema)
async def get_cars(
        page: int = Query(0, ge=0),
        params: ParametersSchema = Depends(validate_parameters),
        cars_service: CarsService = Depends(get_cars_service)
):
    """Получение всех машин по параметрам"""
    return await cars_service.get_cars_with_params_type(page, params)


@router.get("/info", response_model=ResponseCarsType)
async def get_car_info(
        params: ParametersSchema = Depends(validate_parameters),
        cars_service: CarsService = Depends(get_cars_service)
):
    """Получение количество данных о машинах"""
    return await cars_service.get_cars_with_types(params)


@router.get("/{car_id}")
async def get_car(
        car_id: int,
        current_user: Users = Depends(get_current_user),
        cars_service: CarsService = Depends(get_cars_service)
):
    """Выдача всей информации о машине по car_id"""
    return await cars_service.get_car_by_id(car_id, current_user.id)