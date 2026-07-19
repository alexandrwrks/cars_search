from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from database.models import CurrencyType


class CurrencySchema(BaseModel):
    date: date
    base: CurrencyType
    quote: CurrencyType
    rate: Decimal