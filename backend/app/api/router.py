from fastapi import APIRouter

from app.api.auth.handlers import auth_router
from app.api.lots.handlers import lots_router
from app.api.order.handlers import orders_router
from app.api.lots.reading_csv import create_lot_router

# Создание главного роутера API
api_router = APIRouter()

# Подключение отдельных роутеров с соответствующими префиксами
api_router.include_router(auth_router, prefix="/auth", tags=["Аутентификация"])
api_router.include_router(lots_router, prefix="/lots", tags=["Лоты"])
api_router.include_router(create_lot_router, prefix="/lots/upload", tags=["Загрузка лотов"])
api_router.include_router(orders_router, prefix="/orders", tags=["Заказы"]) 