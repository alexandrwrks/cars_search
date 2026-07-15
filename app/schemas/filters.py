from enum import StrEnum
from typing import List

from pydantic import BaseModel, ConfigDict, model_validator, Field


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
