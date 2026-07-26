from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, field_serializer


class ResponseUserSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class ResponseStatisticsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cars_count: int
    active_cars: int
    brands_count: int
    models_count: int
    average_price: int
    average_year: int
    views_count: int
    min_price: int
    max_price: int
    latest_car_date: datetime

    @field_serializer("latest_car_date")
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

class StatisticsSchema(BaseModel):
    name: str | int
    count: int
    avg_price: int

    model_config = ConfigDict(from_attributes=True)

class ResponsePriceHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    price: List[Decimal]
    created_at: List[datetime]