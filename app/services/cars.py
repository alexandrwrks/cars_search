from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.cars import CarsRepository
from app.schemas.filters import ParametersSchema, SortType, FiltersSchema, ResponseParametersSchema, ResponseCarsType


class CarsService:
    def __init__(self, session: AsyncSession):
        self.cars_repo = CarsRepository(session)

    async def get_cars(self, page: int, sort: SortType):
        return await self.cars_repo.get_cars(page, sort)

    async def get_car_by_id(self, car_id: int):
        car_info = await self.cars_repo.get_car_by_id(car_id)
        if car_info is None:
            raise HTTPException(
                status_code=404,
                detail="Car not found"
            )

        return car_info

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

    async def get_cities(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        cities = await self.cars_repo.get_cities(params)
        if not cities:
            return []

        return [
            FiltersSchema(
                name=city,
                count=count
            )
            for city, count in cities
        ]

    async def get_brands(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        brands = await self.cars_repo.get_brands(params)
        if not brands:
            return []

        return [
            FiltersSchema(
                name=brand,
                count=count
            )
            for brand, count in brands
        ]

    async def get_body_types(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        body_types = await self.cars_repo.get_body_types(params)
        if not body_types:
            return []

        return [
            FiltersSchema(
                name=body_type,
                count=count
            )
            for body_type, count in body_types
        ]

    async def get_transmissions(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        transmissions = await self.cars_repo.get_transmissions(params)
        if not transmissions:
            return []

        return [
            FiltersSchema(
                name=transmission,
                count=count
            )
            for transmission, count in transmissions
        ]

    async def get_engine_volumes(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        engine_volumes = await self.cars_repo.get_engine_volumes(params)
        if not engine_volumes:
            return []

        return [
            FiltersSchema(
                name=engine_volume,
                count=count
            )
            for engine_volume, count in engine_volumes
        ]

    async def get_years(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        years = await self.cars_repo.get_years(params)
        if not years:
            return []

        return [
            FiltersSchema(
                name=year,
                count=count
            )
            for year, count in years
        ]

    async def get_models(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        models = await self.cars_repo.get_models(params)
        if not models:
            return []

        return [
            FiltersSchema(
                name=model,
                count=count
            )
            for model, count in models
        ]

    async def get_fuel_types(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        types = await self.cars_repo.get_fuel_types(params)
        if not types:
            return []

        return [
            FiltersSchema(
                name=type,
                count=count
            )
            for type, count in types
        ]

    async def get_colors(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        colors = await self.cars_repo.get_colors(params)
        if not colors:
            return []

        return [
            FiltersSchema(
                name=color,
                count=count
            )
            for color, count in colors
        ]

    async def get_steering(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        steering = await self.cars_repo.get_steering(params)
        if not steering:
            return []

        return [
            FiltersSchema(
                name=side,
                count=count
            )
            for side, count in steering
        ]

    async def get_generations(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        generations = await self.cars_repo.get_generations(params)
        if not generations:
            return []

        return [
            FiltersSchema(
                name=generation,
                count=count
            )
            for generation, count in generations
        ]

    async def get_drives(self, params: ParametersSchema) -> List[FiltersSchema] | List:
        drives = await self.cars_repo.get_drives(params)
        if not drives:
            return []

        return [
            FiltersSchema(
                name=drive,
                count=count
            )
            for drive, count in drives
        ]


    async def get_cars_with_params_type(self, page: int, params: ParametersSchema) -> ResponseParametersSchema:
        cars = await self.cars_repo.get_conditions(page, params)
        total = await self.cars_repo.get_total_cars(params)

        if not cars:
            return ResponseParametersSchema(
                total=0,
                page=0,
                page_size=20,
                items=[]
            )

        return ResponseParametersSchema(
            total=total,
            page=page,
            page_size=len(cars),
            items=cars
        )

