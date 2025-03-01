from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        from_attributes = True

# Схемы для пользователей
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

# Схемы для авторизации
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# разобраться со справочником и другими полями

class ShortShowLots(TunedModel):
    number: int
    code_KSSS_NB: int
    code_KSSS_fuel: int
    current_weight: int
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

class LotsCreate(BaseModel):
    date: datetime
    code_KSSS_NB: Optional[int] = None
    code_KSSS_fuel: Optional[int] = None
    start_weight: Optional[int] = None
    current_weight: Optional[int] = None
    status: Optional[str] = None
    price: Optional[int] = None
    price_for_1ton: Optional[int] = None

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

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

