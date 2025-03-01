from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True

class OrderCreate(BaseModel):
    lot_number: int
    volume: int
    delivery_type: Optional[str] = None

class OrderResponse(TunedModel):
    id: int
    order_date: datetime
    lot_number: int
    code_KSSS_NB: int
    code_KSSS_fuel: int
    volume: int
    delivery_type: Optional[str] = None
    user_id: int