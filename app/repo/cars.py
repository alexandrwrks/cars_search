from typing import List, Dict, Tuple, Any
from sqlalchemy import select, desc, insert, update, text, or_, cast, String, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from database.models import Links, Cars, CarImage
from app.schemas.schemas import CarInfo
from app.schemas.filters import ParametersSchema, SortType

class CarsRepository:
    PAGE_SIZE = 20

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _apply_paginate(self, query: Select, offset: int) -> Select:
        return query.offset(offset * self.PAGE_SIZE).limit(self.PAGE_SIZE)


    async def _aplly_sort(self, query: Select, sort: SortType) -> Select:

        SORT_MAPPING = {
            SortType.newest: desc(Cars.created_at),
            SortType.oldest: Cars.created_at,
            SortType.price_asc: Cars.price,
            SortType.price_desc: desc(Cars.price),
            SortType.year_asc: Cars.year,
            SortType.year_desc: desc(Cars.year),
        }

        return query.order_by(SORT_MAPPING[sort])


    async def _apply_parameters(self, params: ParametersSchema) -> List[Select]:
        conditions = []

        if params.search is not None:
            search_conditions = []

            for part in params.search.split():
                search_conditions.append(
                    or_(
                        Cars.model.ilike(f"%{part}%"),
                        Cars.brand.ilike(f"%{part}%"),
                        Cars.generation.ilike(f"%{part}%"),
                    )
                )

            conditions.extend(search_conditions)

        if params.brand is not None:
            conditions.append(Cars.brand.ilike(f"%{params.brand}%"))

        if params.model is not None:
            conditions.append(Cars.model.ilike(f"%{params.model}%"))

        if params.city is not None:
            conditions.append(Cars.city.ilike(f"%{params.city}%"))

        if params.body_type is not None:
            conditions.append(Cars.body_type.ilike(f"%{params.body_type}%"))

        if params.transmission is not None:
            conditions.append(Cars.transmission.ilike(f"%{params.transmission}%"))

        if params.price_from is not None:
            conditions.append(Cars.price >= params.price_from)

        if params.price_to is not None:
            conditions.append(Cars.price <= params.price_to)

        if params.year_from is not None:
            conditions.append(Cars.year >= params.year_from)

        if params.year_to is not None:
            conditions.append(Cars.year <= params.year_to)

        if params.region is not None:
            conditions.append(Cars.region.ilike(f"%{params.region}%"))

        if params.volume_from is not None:
            conditions.append(Cars.engine_volume >= params.volume_from)

        if params.volume_to is not None:
            conditions.append(Cars.engine_volume <= params.volume_to)

        return conditions


    async def _get_grouped(self, column, params: ParametersSchema) -> List[Tuple[Any, int]]:
        conditions = await self._apply_parameters(params)

        query = (
            select(
                column,
                func.count(Cars.id).label("count")
            )
            .where(
                column.is_not(None),
                Cars.is_active.is_(True),
            )
            .group_by(column)
        )

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query)

        return result.all()


    async def get_cars(self, offset: int, sort: SortType) -> List[Cars]:
        query = (select(Cars))

        query = await self._apply_paginate(query, offset)

        query = await self._aplly_sort(query, sort)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_car_by_id(self, car_id: int) -> Cars | None:
        result = await self.session.execute(
            select(Cars)
            .where(
                Cars.car_id == car_id,
                Cars.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def get_cars_by_search(self, search_term: str, offset: int = 0) -> List[Cars]:
        parts = [part for part in search_term.lower().split() if part]

        conditions = []
        for part in parts:
            conditions.append(
                or_(
                    Cars.model.ilike(f"%{part}%"),
                    Cars.brand.ilike(f"%{part}%"),
                    Cars.generation.ilike(f"%{part}%"),
                    cast(Cars.year, String).ilike(f"%{part}%"),
                )
            )

        query = (
            select(Cars)
            .where(and_(*conditions))
        )

        query = await self._apply_paginate(query, offset)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def add_car_parameters(self, car_id: int, url: str, car: CarInfo):
        await self.session.execute(
            insert(Cars)
            .values(
                car_id=car_id,
                url=url,
                **car.model_dump()
            )
        )

    async def add_car_image(self, values: List[Dict]):
       await self.session.execute(
           insert(CarImage),
           values
       )

    async def change_parse(self, car_id: int):
        await self.session.execute(
            update(Links)
            .where(Links.car_id == car_id)
            .values(parsed=text("true"))
        )

    async def delete(self, car_id: int):
        await self.session.execute(
            update(Links)
            .where(Links.car_id == car_id)
            .values(
                parsed=text("true"),
                is_active=text("false"),
            )
        )

    async def take_car_id(self) -> int:
        result = await self.session.execute(
            select(Links.car_id)
            .where(Links.parsed.is_(False))
        )

        return result.scalars().first()

    async def get_body_types(self, params: ParametersSchema):
        return await self._get_grouped(Cars.body_type, params)

    async def get_cities(self, params: ParametersSchema):
        return await self._get_grouped(Cars.city, params)

    async def get_brands(self, params: ParametersSchema):
        return await self._get_grouped(Cars.brand, params)

    async def get_transmissions(self, params: ParametersSchema):
        return await self._get_grouped(Cars.transmission, params)

    async def get_engine_volumes(self, params: ParametersSchema):
        return await self._get_grouped(Cars.engine_volume, params)

    async def get_years(self, params: ParametersSchema):
        return await self._get_grouped(Cars.year, params)

    async def get_models(self, params: ParametersSchema) -> List[Tuple[str, int]]:
        query = (
            select(
                Cars.model,
                func.count(Cars.id).label("count")
            )
            .where(
                Cars.model.is_not(None),
                Cars.is_active.is_(True),
            )
            .distinct())

        if params.brand is not None:
            query = query.where(and_(Cars.brand.ilike(f"%{params.brand}%")))

        query = query.group_by(Cars.model).order_by(Cars.model)

        result = await self.session.execute(query)

        return result.all()

    async def get_fuel_types(self, params: ParametersSchema):
        return await self._get_grouped(Cars.fuel_type, params)


    async def get_drives(self, params: ParametersSchema):
        return await self._get_grouped(Cars.drive, params)

    async def get_colors(self, params: ParametersSchema):
        return await self._get_grouped(Cars.color, params)

    async def get_steering(self, params: ParametersSchema):
        return await self._get_grouped(Cars.steering, params)

    async def get_generations(self, params: ParametersSchema) -> List[Tuple[str, int]]:
        query = (
            select(
                Cars.generation,
                func.count(Cars.id).label("count")
            )
            .where(
                Cars.generation.is_not(None),
                Cars.is_active.is_(True),
            )
            .group_by(Cars.generation)
            .order_by(Cars.generation)
        )

        if params.brand is not None:
            query = query.where(and_(Cars.brand.ilike(f"%{params.brand}%")))

        if params.model is not None:
            query = query.where(and_(Cars.model.ilike(f"%{params.model}%")))


        result = await self.session.execute(query)

        return result.all()

    async def get_total_cars(self, params: ParametersSchema) -> int:
        query = select(func.count(Cars.id))

        conditions = await self._apply_parameters(params)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query)

        return result.scalar_one()

    async def get_conditions(self, page: int, params: ParametersSchema):
        query = select(Cars)

        conditions = await self._apply_parameters(params)
        query = await self._aplly_sort(query, params.sort)
        query = await self._apply_paginate(query, page)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query)
        return result.scalars().all()
