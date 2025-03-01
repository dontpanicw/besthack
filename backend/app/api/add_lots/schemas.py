from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class LotsCreate(BaseModel):
    date: datetime
    code_KSSS_NB: Optional[int] = None
    code_KSSS_fuel: Optional[int] = None
    start_weight: Optional[int] = None
    current_weight: Optional[int] = None
    status: Optional[str] = None
    price: Optional[int] = None
    price_for_1ton: Optional[int] = None