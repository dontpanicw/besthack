from fastapi import APIRouter
from fastapi import Depends, HTTPException, BackgroundTasks
from sqlalchemy import select, update
from datetime import datetime

from sqlalchemy.orm import Session
from typing import List

from app.repositories import models
from app.repositories.models import Lots, User, Order
from app.settings import engine, get_db
from app.api.auth.security import (
    authenticate_user, create_access_token,
    get_password_hash,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from app.api.lots import schemas
from app.services.lots_service import LotsService, transform_lot_fields

lots_router = APIRouter()

cities = {
    0: "Не указано",
    1: "Москва",
    2: "Санкт-Петербург",
    3: "Екатеринбург",
    4: "Иркутск",
    5: "Владивосток"
}

oil_bases = {
    0: "Не указано",
    1: "Нефтебаза_1",
    2: "Нефтебаза_2",
    3: "Нефтебаза_3",
    4: "Нефтебаза_4",
    5: "Нефтебаза_5"
}

fuel_types = {
    0: "Не указано",
    1: "АИ-92",
    2: "АИ-95",
    3: "АИ-92 Экто",
    4: "АИ-95 Экто",
    5: "ДТ"
}

def update_lot_status(db: Session):
    """Обновляет статус лотов на 'Неактивен', если их дата уже прошла"""
    current_time = datetime.now()
    
    # Находим все лоты со статусом 'Подтвержден', у которых дата истекла
    expired_lots = db.query(models.Lots).filter(
        models.Lots.status == "Подтвержден",
        models.Lots.date < current_time
    ).all()
    
    # Обновляем статус для найденных лотов
    for lot in expired_lots:
        lot.status = "Неактивен"
    
    # Сохраняем изменения в базе данных
    if expired_lots:
        db.commit()

def transform_lot_fields(lot):
    """Преобразует коды в человекочитаемые значения и вычисляет цену за 1 тонну"""
    lot.fuel_type = fuel_types.get(lot.code_KSSS_fuel, "Не указано")
    lot.region_nb = cities.get(lot.code_KSSS_NB, "Не указано")
    lot.nb_name = oil_bases.get(lot.code_KSSS_NB, "Не указано")
    # lot.price_for_1ton = 0

    if lot.start_weight and lot.start_weight > 0:
        lot.price_for_1ton = lot.price / lot.start_weight
    else:
        lot.price_for_1ton = 0
    return lot

@lots_router.get("/", response_model=List[schemas.ShortShowLots])
async def get_lots(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить список лотов с пагинацией
    """
    try:
        lots = LotsService.get_lots(db=db, skip=skip, limit=limit)
        return lots
    except Exception as e:
        # Стандартная обработка ошибок
        raise HTTPException(status_code=500, detail=str(e))

# Оставляем для обратной совместимости, но реализуем отдельную логику фильтрации
@lots_router.get("/filtered-lots", response_model=List[schemas.ShortShowLots])
async def get_filtered_lots(
    skip: int = 0, 
    limit: int = 100, 
    code_KSSS_NB: int = None, 
    code_KSSS_fuel: int = None, 
    db: Session = Depends(get_db)
):
    """
    Получить отфильтрованный список лотов
    """
    try:
        # Создаем фильтрованный запрос
        query = db.query(Lots)
        
        # Добавляем фильтры, если они указаны
        if code_KSSS_NB is not None:
            query = query.filter(Lots.code_KSSS_NB == code_KSSS_NB)
        if code_KSSS_fuel is not None:
            query = query.filter(Lots.code_KSSS_fuel == code_KSSS_fuel)
        
        lots = query.offset(skip).limit(limit).all()
        
        # Преобразуем поля для каждого лота
        for lot in lots:
            transform_lot_fields(lot)
        
        return lots
    except Exception as e:
        # Стандартная обработка ошибок
        raise HTTPException(status_code=500, detail=str(e))

@lots_router.get("/{number}", response_model=schemas.LongShowLots)
async def get_lot_by_number(
    number: int, 
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Получить детальную информацию о лоте по его номеру
    """
    try:
        lot = LotsService.get_lot_by_number(db=db, number=number)
        return lot
    except ValueError as e:
        # Если лот не найден
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Стандартная обработка ошибок
        raise HTTPException(status_code=500, detail=str(e))

@lots_router.post("/", response_model=schemas.LongShowLots)
async def create_lot(
    lot_data: schemas.LotsCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    """
    Создать новый лот (требуются права администратора)
    """
    try:
        new_lot = LotsService.create_lot(db=db, lot_data=lot_data)
        return new_lot
    except ValueError as e:
        # Если данные некорректны
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Стандартная обработка ошибок
        raise HTTPException(status_code=500, detail=str(e))

@lots_router.put("/{number}/status", response_model=schemas.LongShowLots)
async def update_lot_status(
    number: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Обновить статус лота (требуются права администратора)
    """
    try:
        updated_lot = LotsService.update_lot_status(db=db, number=number, status=status)
        return updated_lot
    except ValueError as e:
        # Если лот не найден
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Стандартная обработка ошибок
        raise HTTPException(status_code=500, detail=str(e))