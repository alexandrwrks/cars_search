from fastapi import APIRouter, Depends

from app.deps import get_cars_service
from app.schemas.response import ResponseStatisticsSchema
from app.services.cars import CarsService

router = APIRouter()

@router.get("/", response_model=ResponseStatisticsSchema)
async def get_statistics(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Общая статистика"""
    return await cars_service.get_cars_by_statistics()

@router.get("/brands")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Статистика по брэндам"""
    return await cars_service.get_brand_statistics()

@router.get("/cities")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Статистика по городам"""
    return await cars_service.get_cities_statistics()

@router.get("/years")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Статистика по годам"""
    return await cars_service.get_years_statistics()

@router.get("/popular")
async def get_statistics_brand(
        cars_service: CarsService = Depends(get_cars_service)
):
    """Сама просматриваемая машина"""
    return await cars_service.get_popular_statistics()
