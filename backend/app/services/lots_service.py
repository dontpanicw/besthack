from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.api.lots.schemas import LotsCreate, LongShowLots, ShortShowLots
from app.repositories.models import Lots

class LotsService:
    """Сервис для работы с лотами"""
    
    @staticmethod
    def get_lots(db: Session, skip: int = 0, limit: int = 100) -> List[ShortShowLots]:
        """Получает список лотов с пагинацией"""
        result = db.query(Lots).offset(skip).limit(limit).all()
        return result
    
    @staticmethod
    def get_lot_by_number(db: Session, number: int) -> LongShowLots:
        """Получает лот по номеру"""
        lot = db.query(Lots).filter(Lots.number == number).first()
        if not lot:
            raise ValueError(f"Лот с номером {number} не найден")
        return lot
    
    @staticmethod
    def create_lot(db: Session, lot_data: LotsCreate) -> Lots:
        """Создает новый лот"""
        # Проверка корректности данных
        if lot_data.current_weight is None:
            lot_data.current_weight = lot_data.start_weight
        
        if lot_data.status is None:
            lot_data.status = "Подтвержден"
        
        # Создание объекта лота
        new_lot = Lots(
            date=lot_data.date,
            code_KSSS_NB=lot_data.code_KSSS_NB,
            code_KSSS_fuel=lot_data.code_KSSS_fuel,
            start_weight=lot_data.start_weight,
            current_weight=lot_data.current_weight,
            status=lot_data.status,
            price=lot_data.price,
            price_for_1ton=lot_data.price_for_1ton
        )
        
        # Сохранение в базе данных
        db.add(new_lot)
        db.commit()
        db.refresh(new_lot)
        
        return new_lot
    
    @staticmethod
    def update_lot_status(db: Session, number: int, status: str) -> Lots:
        """Обновляет статус лота"""
        lot = db.query(Lots).filter(Lots.number == number).first()
        if not lot:
            raise ValueError(f"Лот с номером {number} не найден")
        
        lot.status = status
        db.commit()
        db.refresh(lot)
        
        return lot
    
    @staticmethod
    def update_lot_weight(db: Session, number: int, weight_change: int) -> Lots:
        """
        Обновляет текущий вес лота
        weight_change: положительное или отрицательное значение изменения веса
        """
        lot = db.query(Lots).filter(Lots.number == number).first()
        if not lot:
            raise NotFoundException(message=f"Лот с номером {number} не найден")
        
        new_weight = lot.current_weight + weight_change
        
        # Проверка, что новый вес не будет отрицательным
        if new_weight < 0:
            raise BadRequestException(
                message=f"Недостаточный остаток веса. Текущий: {lot.current_weight}, запрошено: {abs(weight_change)}"
            )
        
        # Обновление веса
        lot.current_weight = new_weight
        
        # Если вес стал равен 0, обновляем статус
        if new_weight == 0:
            lot.status = "Продан"
        
        db.commit()
        db.refresh(lot)
        
        return lot 