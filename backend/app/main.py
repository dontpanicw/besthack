from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import List
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm
import csv
import io
from starlette.middleware.cors import CORSMiddleware

from app import schemas
from app.repositories import models
from app.repositories.models import Lots, User
from app.settings import engine, get_db
from app.security import (
    authenticate_user, create_access_token, 
    get_password_hash,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
# get_current_active_user,
app = FastAPI()

# Получаем разрешенные источники из переменных окружения или используем значения по умолчанию
allowed_origins_str = os.getenv("ALLOW_ORIGINS", "*")
origins = allowed_origins_str.split(",") if allowed_origins_str != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/lots", response_model=List[schemas.ShortShowLots])
def get_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lots = db.query(models.Lots).offset(skip).limit(limit).all()
    return lots

@app.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что файл имеет расширение .csv
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Загруженный файл должен быть в формате CSV")
    
    try:
        # Считываем содержимое файла
        contents = await file.read()
        decoded_content = contents.decode('utf-8')
        
        # Определяем названия полей
        fieldnames = ['lot_date', 'ksss_nb_code', 'ksss_fuel_code', 'start_volume_liters', 'available', 'price', 'price_for_1ton']
        
        # Создаем CSV reader
        reader = csv.DictReader(io.StringIO(decoded_content), fieldnames=fieldnames)
        
        # Пропускаем заголовок, если он есть
        has_header = True
        try:
            first_line = next(reader)
            # Если первая строка похожа на заголовок (содержит названия полей)
            if first_line and all(key in first_line.values() for key in fieldnames):
                has_header = True
            else:
                # Если это не заголовок, а данные, сбрасываем reader и обрабатываем эту строку
                reader = csv.DictReader(io.StringIO(decoded_content), fieldnames=fieldnames)
                has_header = False
        except StopIteration:
            # Если файл пустой
            return {"status": "error", "detail": "Загруженный файл не содержит данных"}
        
        # Счетчики для статистики
        processed_rows = 0
        skipped_rows = 0
        errors = []
        
        # Обрабатываем каждую строку
        for row_num, row in enumerate(reader, 1):
            try:
                # Пропускаем заголовок, если он есть
                if row_num == 1 and has_header:
                    continue
                
                # Преобразуем данные
                try:
                    # Пробуем разные форматы даты
                    date_formats = ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y']
                    lot_date = None
                    
                    for date_format in date_formats:
                        try:
                            lot_date = datetime.strptime(row['lot_date'], date_format)
                            break
                        except ValueError:
                            continue
                    
                    if lot_date is None:
                        raise ValueError(f"Неверный формат даты: {row['lot_date']}")
                    
                    # Создаем новый лот
                    lot = models.Lots(
                        date=lot_date,
                        code_KSSS_NB=int(row['ksss_nb_code']),
                        code_KSSS_fuel=int(row['ksss_fuel_code']),
                        start_weight=int(row['start_volume_liters']),
                        current_weight=int(row['start_volume_liters']),
                        status="Подтвержден" ,
                        price=int(row['price']),  # Значение по умолчанию
                        price_for_1ton=int(row['price_for_1ton'])  # Значение по умолчанию
                    )
                    
                    # Добавляем в сессию
                    db.add(lot)
                    processed_rows += 1
                
                except (ValueError, TypeError) as e:
                    skipped_rows += 1
                    errors.append(f"Строка {row_num}: {str(e)}")
                    continue
                
            except Exception as e:
                # Если возникла ошибка при обработке строки, пропускаем её
                skipped_rows += 1
                errors.append(f"Строка {row_num}: Непредвиденная ошибка - {str(e)}")
                continue
        
        # Сохраняем все изменения в базе данных
        db.commit()
        
        response = {
            "status": "success",
            "filename": file.filename,
            "processed_rows": processed_rows,
            "skipped_rows": skipped_rows
        }
        
        if errors:
            response["errors"] = errors[:10]  # Возвращаем только первые 10 ошибок
            if len(errors) > 10:
                response["errors"].append(f"... и еще {len(errors) - 10} ошибок")
        
        return response
        
    except Exception as e:
        # В случае ошибки откатываем транзакцию
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")

@app.get("/lot/{number}", response_model=schemas.LongShowLots)
async def show_lot(number: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = db.execute(select(Lots).where(Lots.number == number))
    lot = result.scalars().first()
    if not lot:
        raise HTTPException(status_code=404, detail=f"Event with number {number} not found")
    return lot

