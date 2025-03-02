from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import select

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

lots_router = APIRouter()

cities = {
    1: "Москва",
    2: "Санкт-Петербург",
    3: "Екатеринбург",
    4: "Иркутск",
    5: "Владивосток"
}

oil_bases = {
    1: "Нефтебаза_1",
    2: "Нефтебаза_2",
    3: "Нефтебаза_3",
    4: "Нефтебаза_4",
    5: "Нефтебаза_5"
}

fuel_types = {
    1: "АИ-92",
    2: "АИ-95",
    3: "АИ-92 Экто",
    4: "АИ-95 Экто",
    5: "ДТ"
}

@lots_router.get("/lots", response_model=List[schemas.ShortShowLots])
def get_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    for lot in db.query(models.Lots).offset(skip).limit(limit).all():
        lot.fuel_type = fuel_types[lot.code_KSSS_fuel]
        lot.region_nb = cities[lot.code_KSSS_NB]
        lot.nb_name = oil_bases[lot.code_KSSS_NB]
        lot.price_for_1ton = lot.price / lot.start_weight
    
    lots = db.query(models.Lots).offset(skip).limit(limit).all()
    # lots = db.query(models.Lots).offset(skip).limit(limit).all()
    return lots

@lots_router.post("/lot", response_model=schemas.LongShowLots)
def create_lot(lot: schemas.LotsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_lots = models.Lots(
    date = lot.date,
    code_KSSS_NB = lot.code_KSSS_NB,
    code_KSSS_fuel = lot.code_KSSS_fuel,
    start_weight = lot.start_weight,
    current_weight = lot.current_weight,
    status = lot.status,
    price = lot.price,
    price_for_1ton = lot.price_for_1ton)
    db.add(db_lots)
    db.commit()
    db.refresh(db_lots)
    return db_lots

@lots_router.get("/lot/{number}", response_model=schemas.LongShowLots)
async def show_lot(number: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.execute(select(Lots).where(Lots.number == number))
    lot = result.scalars().first()
    if not lot:
        raise HTTPException(status_code=404, detail=f"Event with number {number} not found")
    return lot