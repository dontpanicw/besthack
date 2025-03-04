from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True

class LotsCreate(BaseModel):
    date: datetime
    code_KSSS_NB: Optional[int] = None
    code_KSSS_fuel: Optional[int] = None
    start_weight: Optional[int] = None
    current_weight: Optional[int] = None
    status: Optional[str] = None
    price: Optional[int] = None
    price_for_1ton: Optional[int] = None


class ShortShowLots(TunedModel):
    number: int
    fuel_type: str
    region_nb: str
    nb_name: str
    price_for_1ton: int

class LongShowLots(TunedModel):
    number: int
    date: datetime
    code_KSSS_NB: Optional[int] = None
    code_KSSS_fuel: Optional[int] = None
    start_weight: Optional[int] = None
    current_weight: Optional[int] = None
    status: Optional[str] = None
    price: Optional[int] = None
    price_for_1ton: Optional[int] = None