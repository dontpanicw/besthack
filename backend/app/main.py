from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import List
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.repositories import models
from app.repositories.models import Lots, User
from app.settings import engine, get_db
from app.security import (
    authenticate_user, create_access_token, 
    get_password_hash,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
# get_current_active_user,
app = FastAPI()

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
#
# # Создаем движок SQLAlchemy
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

@app.get("/root")
async def root():
    return {"message": "FastAPI с SQLAlchemy успешно запущен!"}

# Эндпоинты для аутентификации
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверка на существование пользователя с таким email
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    # Создание нового пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # В OAuth2PasswordRequestForm поле называется username, но мы будем использовать его для email
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/lot", response_model=schemas.LongShowLots)
def create_user(lot: schemas.LotsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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

@app.get("/lots", response_model=List[schemas.ShortShowLots])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    lots = db.query(models.Lots).offset(skip).limit(limit).all()
    return lots

@app.get("/events/{event_id}", response_model=schemas.LongShowLots)
async def show_event(number: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.execute(select(Lots).where(Lots.number == number))
    lot = result.scalars().first()
    if not lot:
        raise HTTPException(status_code=404, detail=f"Event with number {number} not found")
    return lot

