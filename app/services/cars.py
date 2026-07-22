from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.cars import CarsRepository
from app.schemas.filters import (FiltersSchema, FullCarResponse,
                                 ParametersSchema, PopularCarResponse,
                                 ResponseCarsType, ResponseParametersSchema,
                                 SortType)
from app.schemas.response import ResponseStatisticsSchema, StatisticsSchema
from services.cache.cache_service import CacheService
from utils.logger import logger


class CarsService:
    def __init__(self, session: AsyncSession, cache: CacheService):
        self.cars_repo = CarsRepository(session)
        self.cache = cache

    async def get_cars(self, page: int, sort: SortType):
        return await self.cars_repo.get_cars(page, sort)

    async def get_car_by_id(self, car_id: int, user_id: int) -> FullCarResponse:
        key = f"car:{car_id}"
        cached = await self.cache.get(key, FullCarResponse)

        if cached:
            logger.info("REDIS: card_id=%s", key)
            return cached

        car = await self.cars_repo.get_car_by_id(car_id)
        if car is None:
            raise HTTPException(
                status_code=404,
                detail="Car not found"
            )

        view_id = await self.cars_repo.register_view(car_id, user_id)
        if view_id is not None:
            await self.cars_repo.add_view(car_id)

        response = FullCarResponse.model_validate(car)

        await self.cache.set(
            key,
            value=response.model_dump(mode="json"),
            expire=3600
        )

        return response

    async def get_cars_with_parameters(self, params: ParametersSchema) -> int:
        total = await self.cars_repo.get_total_cars(params)
        if not total:
            return 0

        return total


    async def get_cars_with_types(self, params: ParametersSchema):
        return ResponseCarsType(
            total=await self.get_cars_with_parameters(params),
            city=await self.get_cities(params),
            brand=await self.get_brands(params),
            model=await self.get_models(params),
            body_types=await self.get_body_types(params),
            transmissions=await self.get_transmissions(params),
            engine_volumes=await self.get_engine_volumes(params),
            years=await self.get_years(params),
            fuel_type=await self.get_fuel_types(params),
            color=await self.get_colors(params),
            steering=await self.get_steering(params),
            generation=await self.get_generations(params),
            drive=await self.get_drives(params)
    )

    async def get_cities(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=city, count=count)
            for city, count in await self.cars_repo.get_cities(params)
        ]

    async def get_brands(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=brand, count=count)
            for brand, count in await self.cars_repo.get_brands(params)
        ]

    async def get_body_types(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=body_type, count=count)
            for body_type, count in await self.cars_repo.get_body_types(params)
        ]

    async def get_transmissions(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=transmission, count=count)
            for transmission, count in await self.cars_repo.get_transmissions(params)
        ]

    async def get_engine_volumes(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=engine_volume, count=count)
            for engine_volume, count in await self.cars_repo.get_engine_volumes(params)
        ]

    async def get_years(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=year, count=count)
            for year, count in await self.cars_repo.get_years(params)
        ]

    async def get_models(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=model, count=count)
            for model, count in await self.cars_repo.get_models(params)
        ]

    async def get_fuel_types(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=fuel, count=count)
            for fuel, count in  await self.cars_repo.get_fuel_types(params)
        ]

    async def get_colors(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=color, count=count)
            for color, count in await self.cars_repo.get_colors(params)
        ]

    async def get_steering(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=side, count=count)
            for side, count in await self.cars_repo.get_steering(params)
        ]

    async def get_generations(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=generation, count=count)
            for generation, count in await self.cars_repo.get_generations(params)
        ]

    async def get_drives(self, params: ParametersSchema) -> List[FiltersSchema]:
        return [
            FiltersSchema(name=drive, count=count)
            for drive, count in await self.cars_repo.get_drives(params)
        ]


    async def get_cars_with_params_type(self, page: int, params: ParametersSchema) -> ResponseParametersSchema:
        key = f"cars:{page}:{params.model_dump_json()}"
        cached = await self.cache.get(key, ResponseParametersSchema)

        if cached:
            logger.info("REDIS: cars=%s", key)
            return cached

        cars = await self.cars_repo.get_conditions(page, params)
        total = await self.cars_repo.get_total_cars(params)

        response = ResponseParametersSchema(
            total=total,
            page=page,
            page_size=len(cars),
            items=cars
        )

        await self.cache.set(
            key,
            response.model_dump(mode="json"),
            expire=3600
        )

        if not cars:
            return ResponseParametersSchema(
                total=0,
                page=0,
                page_size=0,
                items=[]
            )

        return ResponseParametersSchema(
            total=total,
            page=page,
            page_size=len(cars),
            items=cars
        )

    async def get_cars_by_statistics(self) -> ResponseStatisticsSchema:
        """
        Return all statistics for cars

        :return
            ResponseStatisticsSchema
        """
        key = f"cars:statistics"

        cached = await self.cache.get(key, ResponseStatisticsSchema)
        if cached:
            return cached

        cars = await self.cars_repo.get_statics()

        response = ResponseStatisticsSchema.model_dump(cars)

        await self.cache.set(
            key,
            response,
            expire=900
        )

        return response

    async def get_brand_statistics(self) -> List[StatisticsSchema]:
        key = f"brands:statistics"
        cached = await self.cache.get(key, StatisticsSchema, many=True)

        if cached:
            return cached

        items = await self.cars_repo.get_brand_statistics()

        response = [
            StatisticsSchema.model_validate(item)
            for item in items
        ]

        await self.cache.set(
            key,
            response,
            expire=900
        )

        return response

    async def get_cities_statistics(self) -> List[StatisticsSchema]:
        key = f"cities:statistics"
        cached = await self.cache.get(key, StatisticsSchema, many=True)

        if cached:
            return cached

        items = await self.cars_repo.get_cities_statistics()

        response = [
            StatisticsSchema.model_validate(item)
            for item in items
        ]

        await self.cache.set(
            key,
            response,
            expire=900
        )

        return response

    async def get_years_statistics(self) -> List[StatisticsSchema]:
        key = f"years:statistics"
        cached = await self.cache.get(key, StatisticsSchema, many=True)

        if cached:
            return cached

        items = await self.cars_repo.get_years_statistics()

        response = [
            StatisticsSchema.model_validate(item)
            for item in items
        ]

        await self.cache.set(
            key,
            response,
            expire=900
        )

        return response

    async def get_popular_statistics(self) -> List[PopularCarResponse]:
        key = f"popular:statistics"
        cached = await self.cache.get(key, PopularCarResponse, many=True)

        if cached:
            return cached

        cars = await self.cars_repo.get_popular_car()

        response = [
            PopularCarResponse.model_validate(car)
            for car in cars
        ]

        await self.cache.set(
            key,
            response,
            expire=900
        )

        return response