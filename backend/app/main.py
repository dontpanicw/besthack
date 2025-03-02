from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.repositories import models
from app.settings import engine, get_db
from app.core.exception_handlers import add_exception_handlers
from app.api.router import api_router

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
    application.include_router(api_router, prefix="/api")
    
    # Добавление обработчиков исключений
    add_exception_handlers(application)
    
    # Создание таблиц в базе данных (для разработки)
    models.Base.metadata.create_all(bind=engine)
    
    return application

app = create_application()

@app.get("/health")
async def health():
    """Эндпоинт для проверки работы сервиса"""
    return {"status": "ok"}




