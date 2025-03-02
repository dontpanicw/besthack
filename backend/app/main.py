from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.repositories import models
from app.settings import engine, get_db

from app.api.lots.handlers import lots_router

from app.api.order.handlers import orders_router

from app.api.auth.handlers import auth_router

from app.api.lots.reading_csv import create_lot_router

app = FastAPI(title="fuel exchange")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://31.130.150.30:8000", "http://31.130.150.30", "http://localhost",
                   "http://31.130.150.30:3000", "http://31.130.150.30:80", "http://localhost:80",
                   "http://localhost:8000/lots"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, tags=["Auth"])

app.include_router(lots_router, tags=["Lots"])

app.include_router(create_lot_router, tags=["CreateLot"])

app.include_router(orders_router, tags=["Orders"])


models.Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"ok"}




