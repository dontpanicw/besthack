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
from app.repositories.models import Lots, User, Order
from app.settings import engine, get_db
from app.security import (
    authenticate_user, create_access_token, 
    get_password_hash,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.data_validation import get_price_validation_ranges

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://31.130.150.30:8000", "http://31.130.150.30", "http://localhost"],  # Список разрешенных источников
    allow_credentials=True,  # Разрешить передачу credentials (cookies, заголовки авторизации)
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

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

@app.get("/lots", response_model=List[schemas.ShortShowLots])
def get_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lots = db.query(models.Lots).offset(skip).limit(limit).all()
    return lots

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
        # Получаем допустимые диапазоны цен на основе имеющихся данных
        price_ranges = get_price_validation_ranges(db)
        
        # Считываем содержимое файла
        contents = await file.read()
        decoded_content = contents.decode('utf-8')
        
        # Определяем названия полей
        fieldnames = ['lot_date', 'ksss_nb_code', 'ksss_fuel_code', 'start_volume_liters', 'price', 'price_for_1ton']
        
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
                    
                    # Преобразуем значения цен в числа
                    price = int(row['price'])
                    price_for_1ton = int(row['price_for_1ton'])
                    
                    # Проверяем соответствие цен допустимым диапазонам
                    price_in_range = True
                    price_error_message = ""
                    
                    # Проверка price, если есть данные для сравнения
                    if price_ranges['price']['min'] is not None and price_ranges['price']['max'] is not None:
                        if price < price_ranges['price']['min'] or price > price_ranges['price']['max']:
                            price_in_range = False
                            price_error_message += f"Цена ({price}) находится вне допустимого диапазона ({int(price_ranges['price']['min'])} - {int(price_ranges['price']['max'])}). "
                    
                    # Проверка price_for_1ton, если есть данные для сравнения
                    if price_ranges['price_for_1ton']['min'] is not None and price_ranges['price_for_1ton']['max'] is not None:
                        if price_for_1ton < price_ranges['price_for_1ton']['min'] or price_for_1ton > price_ranges['price_for_1ton']['max']:
                            price_in_range = False
                            price_error_message += f"Цена за 1 тонну ({price_for_1ton}) находится вне допустимого диапазона ({int(price_ranges['price_for_1ton']['min'])} - {int(price_ranges['price_for_1ton']['max'])})."
                    
                    # Если цены не соответствуют диапазону, пропускаем запись
                    if not price_in_range:
                        skipped_rows += 1
                        errors.append(f"Строка {row_num}: {price_error_message}")
                        continue
                    
                    # Создаем новый лот
                    lot = models.Lots(
                        date=lot_date,
                        code_KSSS_NB=int(row['ksss_nb_code']),
                        code_KSSS_fuel=int(row['ksss_fuel_code']),
                        start_weight=int(row['start_volume_liters']),
                        current_weight= int(row['start_volume_liters']),
                        status="Подтвержден",
                        price=price,
                        price_for_1ton=price_for_1ton
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
        
        # Формируем дополнительную информацию о диапазонах цен
        price_info = {}
        if price_ranges['price']['avg'] is not None:
            price_info['price_avg'] = price_ranges['price']['avg']
            price_info['price_min'] = price_ranges['price']['min']
            price_info['price_max'] = price_ranges['price']['max']
        
        if price_ranges['price_for_1ton']['avg'] is not None:
            price_info['price_for_1ton_avg'] = price_ranges['price_for_1ton']['avg']
            price_info['price_for_1ton_min'] = price_ranges['price_for_1ton']['min']
            price_info['price_for_1ton_max'] = price_ranges['price_for_1ton']['max']
        
        response = {
            "status": "success",
            "filename": file.filename,
            "processed_rows": processed_rows,
            "skipped_rows": skipped_rows,
            "price_ranges": price_info
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

@app.post("/order", response_model=schemas.OrderResponse)
async def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Получаем лот из БД
    lot = db.query(Lots).filter(Lots.number == order.lot_number).first()
    if not lot:
        raise HTTPException(status_code=404, detail=f"Лот с номером {order.lot_number} не найден")
    
    # Проверяем, что запрашиваемый объем не превышает доступный вес
    if order.volume > lot.current_weight:
        raise HTTPException(
            status_code=400, 
            detail=f"Запрашиваемый объем ({order.volume}) превышает доступный ({lot.current_weight})"
        )
    
    # Создаем новый заказ
    new_order = Order(
        lot_number=order.lot_number,
        code_KSSS_NB=lot.code_KSSS_NB,
        code_KSSS_fuel=lot.code_KSSS_fuel,
        volume=order.volume,
        delivery_type=order.delivery_type,
        user_id=current_user.id
    )
    
    # Вычитаем объем заказа из текущего веса лота
    lot.current_weight -= order.volume
    
    # Если текущий вес стал равен 0, меняем статус на "Продан"
    if lot.current_weight == 0:
        lot.status = "Продан"
    
    # Сохраняем изменения
    db.add(new_order)
    db.commit()
    
    # Обновляем данные заказа, чтобы вернуть актуальную информацию
    db.refresh(new_order)
    
    return new_order

@app.get("/orders/my", response_model=List[schemas.OrderResponse])
async def get_my_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Получаем заказы текущего пользователя
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    return orders

@app.get("/orders", response_model=List[schemas.OrderResponse])
async def get_all_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin_user)
):
    # Для админов - получение всех заказов
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@app.post("/create_admin", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверка на существование пользователя с таким email
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    # Создание нового пользователя
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_admin=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

