from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List



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

from app.api.order import schemas

orders_router = APIRouter()

@orders_router.post("/order", response_model=schemas.OrderResponse)
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


@orders_router.get("/orders/my", response_model=List[schemas.OrderResponse])
async def get_my_orders(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Получаем заказы текущего пользователя
    orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    return orders


@orders_router.get("/orders", response_model=List[schemas.OrderResponse])
async def get_all_orders(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_admin_user)
):
    # Для админов - получение всех заказов
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders