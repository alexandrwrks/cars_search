from pydantic import BaseModel

class CarInfo(BaseModel):
    brand: str
    model: str
    generation: str | None = None

    year: int

    price: int

    city: str
    region: str | None = None

    body_type: str | None = None

    engine_volume: float | None = None
    fuel_type: str | None = None

    transmission: str | None = None
    drive: str | None = None
    steering: str | None = None

    color: str | None = None

    customs_cleared: bool

    description: str | None = None

    options: list[str]


class CarImages(BaseModel):
    images: list[str]

class ParsedCar(BaseModel):
    car_id: int
    car: CarInfo
    images: CarImages