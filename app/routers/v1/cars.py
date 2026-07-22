from fastapi import APIRouter, Depends, Query

from app.deps import get_cars_service, get_current_user, validate_parameters
from app.schemas.filters import (FullCarResponse, ParametersSchema,
                                 ResponseCarsType, ResponseParametersSchema)
from app.schemas.response import ResponseStatisticsSchema
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

@router.get("/statisctics", response_model=ResponseStatisticsSchema)
async def get_statistics(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Общая статистика"""
    return await cars_service.get_cars_by_statistics()

@router.get("/statistics/brands")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Статистика по брэндам"""
    return await cars_service.get_brand_statistics()

@router.get("/statistics/cities")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Статистика по городам"""
    return await cars_service.get_cities_statistics()

@router.get("/statistics/years")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Статистика по годам"""
    return await cars_service.get_years_statistics()

@router.get("/statistics/popular")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Сама просматриваемая машина"""
    return await cars_service.get_popular_statistics()


@router.get("/{car_id}", response_model=FullCarResponse)
async def get_car(
        car_id: int,
        current_user: Users = Depends(get_current_user),
        cars_service: CarsService = Depends(get_cars_service)
):
    """Выдача всей информации о машине по car_id"""
    return await cars_service.get_car_by_id(car_id, current_user.id)