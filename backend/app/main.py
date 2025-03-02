from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.repositories import models
from app.settings import engine, get_db
# Удаляем импорт обработчиков исключений
# from app.core.exception_handlers import add_exception_handlers
from app.api.router import api_router
from app.api.auth.security import (
    authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.api.auth import schemas
from sqlalchemy.orm import Session

def create_application() -> FastAPI:
    """Фабричная функция для создания и настройки приложения FastAPI"""
    application = FastAPI(
        title="Fuel Exchange API",
        description="API для биржи топлива",
        version="1.0.0"
    )
    
    # Настройка CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000", 
            "http://31.130.150.30:8000", 
            "http://31.130.150.30", 
            "http://localhost",
            "http://31.130.150.30:3000", 
            "http://31.130.150.30:80", 
            "http://localhost:80",
            "http://localhost:8000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Добавление роутеров API
    application.include_router(api_router)
    
    # Удаляем добавление обработчиков исключений
    # add_exception_handlers(application)
    
    # Создание таблиц в базе данных (для разработки)
    models.Base.metadata.create_all(bind=engine)
    
    return application

app = create_application()

@app.get("/health")
async def health():
    """Эндпоинт для проверки работы сервиса"""
    return {"status": "ok"}

# Дополнительный эндпоинт для аутентификации без префикса /auth
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # В OAuth2PasswordRequestForm поле называется username, но используем его для email
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




