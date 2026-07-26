from typing import Any, Dict, List, Tuple

from sqlalchemy import (String, and_, cast, cte, desc, func, or_, select, text,
                        update)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select

from app.schemas.filters import ParametersSchema, SortType
from app.schemas.response import ResponseStatisticsSchema
from app.schemas.schemas import CarInfo
from database.models import CarImage, Cars, Links, PriceHistory


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
            .options(selectinload(Cars.images))
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

    async def add_car_parameters(self, car_id: int, url: str, car: CarInfo, currency: str):
        await self.session.execute(
            insert(Cars)
            .values(
                car_id=car_id,
                url=url,
                currency=currency,
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

    async def get_total_cars(self, params: ParametersSchema | None = None) -> int:
        query = select(func.count(Cars.id))
        if params is not None:
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

    async def register_view(self, car_id: int, user_id: int) -> int | None:
        query = text(
            """
            INSERT INTO car_views (car_id, user_id)
            VALUES (:car_id, :user_id)
            ON CONFLICT (car_id, user_id)
            DO NOTHING
            RETURNING id
            """
        )

        result = await self.session.execute(
            query,
            {
                "car_id": car_id,
                "user_id": user_id,
            }
        )
        return result.scalar_one_or_none()

    async def add_view(self, car_id: int):
        await self.session.execute(
            update(Cars)
            .where(Cars.car_id == car_id)
            .values(
                views = Cars.views + 1,
            )
        )

    async def get_statics(self):
        """Получение данных для статистики"""
        return ResponseStatisticsSchema(
            cars_count=await self.get_total_cars(),
            active_cars=await self.get_active_total_cars(),
            brands_count=await self.get_total_brands(),
            models_count=await self.get_total_models(),
            average_price=await self.get_average_price(),
            average_year=await self.get_average_years(),
            views_count=await self.get_total_views(),
            min_price=await self.get_min_price(),
            max_price=await self.get_max_price(),
            latest_car_date=await self.get_latest_car_date(),
        )

    async def get_active_total_cars(self) -> int:
        result = await self.session.execute(
            select(func.count(Cars.id))
            .where(Cars.is_active.is_(True))
        )
        return result.scalar_one()

    async def get_total_brands(self) -> int:
        result = await self.session.execute(
            select(func.count(Cars.brand.distinct()))
            .where(Cars.is_active.is_(True))
        )
        return result.scalar_one()

    async def get_total_models(self) -> int:
        result = await self.session.execute(
            select(func.count(Cars.model.distinct()))
            .where(Cars.is_active.is_(True))
        )
        return result.scalar_one()

    async def get_average_price(self) -> int:
        result = await self.session.execute(
            select(func.round(func.avg(Cars.price), 0))
            .where(Cars.is_active.is_(True))
        )

        return result.scalar_one()

    async def get_average_years(self) -> int:
        result = await self.session.execute(
            select(func.round(func.avg(Cars.year), 0))
            .where(Cars.is_active.is_(True))
        )

        return result.scalar_one()

    async def get_total_views(self) -> int:
        result = await self.session.execute(select(func.sum(Cars.views)))
        return result.scalar_one()

    async def get_min_price(self) -> int:
        result = await self.session.execute(
            select(func.min(Cars.price))
            .where(Cars.is_active.is_(True))
        )

        return result.scalar_one()

    async def get_max_price(self) -> int:
        result = await self.session.execute(
            select(func.max(Cars.price))
            .where(Cars.is_active.is_(True))
        )

        return result.scalar_one()

    async def get_latest_car_date(self):
        result = await self.session.execute(
            select(func.max(Cars.created_at))
            .where(Cars.is_active.is_(True))
        )
        return result.scalar_one()

    async def _get_statistics(self, column) -> List[Tuple[str, int, int]]:
        result = await self.session.execute(
            select(
                column.label("name"),
                func.count(Cars.id).label("count"),
                func.round(func.avg(Cars.price), 0).label("avg_price"),
            )
            .where(Cars.is_active.is_(True))
            .group_by(column)
        )

        return result.all()

    async def get_brand_statistics(self):
        return await self._get_statistics(Cars.brand)

    async def get_cities_statistics(self):
        return await self._get_statistics(Cars.city)

    async def get_years_statistics(self):
        return await self._get_statistics(Cars.year)

    async def get_popular_car(self) -> List[Cars]:
        result = await self.session.execute(
            select(Cars)
            .where(Cars.is_active.is_(True))
            .order_by(Cars.views.desc())
            .limit(10)
        )
        return result.scalars().all()

    async def get_the_price_change_history(self, car_id: int) -> List[PriceHistory]:
        result = await self.session.execute(
            select(PriceHistory)
            .where(PriceHistory.car_id == car_id)
            .order_by(PriceHistory.created_at)
        )

        return result.scalars().all()