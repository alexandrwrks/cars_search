from datetime import datetime
from enum import StrEnum
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from database.models import CurrencyType


class SortType(StrEnum):
    newest = 'newest'
    oldest = 'oldest'
    price_asc = "price_asc"
    price_desc = "price_desc"
    year_asc = "year_asc"
    year_desc = "year_desc"



class ParametersSchema(BaseModel):
    search: str | None = None
    brand: str | None = None
    model: str | None = None

    city: str | None = None

    body_type: str | None = None

    transmission: str | None = None

    price_from: int | None = Field(None, ge=0) # Нижняя планка
    price_to: int | None = Field(None, ge=0) # Верхняя планка

    year_from: int | None = Field(None, ge=1990)
    year_to: int | None = Field(None, ge=1990)

    region: str | None = None
    volume_from: float | None = Field(None, ge=0)
    volume_to: float | None = Field(None, ge=0)

    sort: SortType = SortType.newest



class FiltersSchema(BaseModel):
    name: str | int | float
    count: int


class CarResponse(BaseModel):
    car_id: int
    brand: str
    model: str
    year: int
    price: int
    city: str

    model_config = ConfigDict(from_attributes=True)

class CarImageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    car_id: int
    position: int
    image_url: str

class FullCarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    car_id: int
    url: str

    is_active: bool

    brand: str
    model: str
    generation: str | None

    year: int
    price: int
    currency: CurrencyType

    city: str
    region: str | None

    body_type: str

    engine_volume: float
    fuel_type:str | None

    transmission: str

    drive: str

    steering: str

    color: str | None

    customs_cleared: bool

    description: str | None

    seller_phone: str | None

    options: List[str]

    created_at: datetime
    updated_at: datetime

    images: List[CarImageSchema]

class ResponseParametersSchema(BaseModel):
    total: int
    page: int
    page_size: int = 20
    items: List[CarResponse] | None = None

class ResponseCarsType(BaseModel):
    total: int
    city: List
    brand: List
    model: List
    body_types: List
    transmissions: List
    engine_volumes: List
    years: List
    fuel_type: List
    color: List
    steering: List
    generation: List
    drive: List
