from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.api.lots.schemas import LotsCreate, LongShowLots, ShortShowLots
from app.repositories.models import Lots

# Данные для преобразования кодов в человекочитаемые значения
cities = {
    0: "Не указано",
    1: "Москва",
    2: "Санкт-Петербург",
    3: "Екатеринбург",
    4: "Иркутск",
    5: "Владивосток"
}

oil_bases = {
    0: "Не указано",
    1: "Нефтебаза_1",
    2: "Нефтебаза_2",
    3: "Нефтебаза_3",
    4: "Нефтебаза_4",
    5: "Нефтебаза_5"
}

fuel_types = {
    0: "Не указано",
    1: "АИ-92",
    2: "АИ-95",
    3: "АИ-92 Экто",
    4: "АИ-95 Экто",
    5: "ДТ"
}

def transform_lot_fields(lot):
    """Преобразует коды в человекочитаемые значения и вычисляет цену за 1 тонну"""
    lot.fuel_type = fuel_types.get(lot.code_KSSS_fuel, "Не указано")
    lot.region_nb = cities.get(lot.code_KSSS_NB, "Не указано")
    lot.nb_name = oil_bases.get(lot.code_KSSS_NB, "Не указано")
    lot.price_for_1ton = lot.price_for_1ton

    # if lot.start_weight and lot.start_weight > 0:
    #     lot.price_for_1ton = lot.price / lot.start_weight
    # else:
    #     lot.price_for_1ton = 0
    return lot

class LotsService:
    """Сервис для работы с лотами"""
    
    @staticmethod
    def get_lots(db: Session, skip: int = 0, limit: int = 100) -> List[ShortShowLots]:
        """Получает список лотов с пагинацией"""
        lots = db.query(Lots).offset(skip).limit(limit).all()
        
        # Преобразуем поля для каждого лота
        for lot in lots:
            transform_lot_fields(lot)
            
        return lots
    
    @staticmethod
    def get_lot_by_number(db: Session, number: int) -> LongShowLots:
        """Получает лот по номеру"""
        lot = db.query(Lots).filter(Lots.number == number).first()
        if not lot:
            raise ValueError(f"Лот с номером {number} не найден")
        
        # Преобразуем поля лота
        transform_lot_fields(lot)
        
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
            status="Подтвержден",
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
            raise ValueError(f"Лот с номером {number} не найден")
        
        new_weight = lot.current_weight + weight_change
        
        # Проверка, что новый вес не будет отрицательным
        if new_weight < 0:
            raise ValueError(
                f"Недостаточный остаток веса. Текущий: {lot.current_weight}, запрошено: {abs(weight_change)}"
            )
        
        # Обновление веса
        lot.current_weight = new_weight
        
        # Если вес стал равен 0, обновляем статус
        if new_weight == 0:
            lot.status = "Продан"
        
        db.commit()
        db.refresh(lot)
        
        # Преобразуем поля лота перед возвратом
        transform_lot_fields(lot)
        
        return lot 