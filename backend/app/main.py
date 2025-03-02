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
    application = FastAPI(
        title="Fuel Exchange",
        description="Биржа топлива",
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
    
    application.include_router(api_router)

    models.Base.metadata.create_all(bind=engine)
    
    return application

app = create_application()

@app.get("/health")
async def health():
    return {"status": "ok"}




