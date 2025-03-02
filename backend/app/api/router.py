from fastapi import APIRouter

from app.api.auth.handlers import auth_router
from app.api.lots.handlers import lots_router
from app.api.order.handlers import orders_router
from app.api.lots.reading_csv import create_lot_router

api_router = APIRouter()

# Основные роутеры с префиксами
api_router.include_router(auth_router, prefix="/auth", tags=["Аутентификация"])
api_router.include_router(lots_router, prefix="/lots", tags=["Лоты"])
api_router.include_router(create_lot_router, prefix="/lots/upload", tags=["Загрузка лотов"])
api_router.include_router(orders_router, prefix="/orders", tags=["Заказы"])

# Дублируем роутер аутентификации без префикса для совместимости с фронтендом
api_router.include_router(auth_router, tags=["Аутентификация-Совместимость"]) 