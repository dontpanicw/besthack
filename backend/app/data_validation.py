from sqlalchemy.orm import Session
import statistics
from app.repositories.models import Lots

def get_price_validation_ranges(db: Session):
    """
    Получает допустимые диапазоны цен на основе имеющихся данных в БД.
    Диапазон составляет от 0.5*среднее до 2*среднее.
    
    Возвращает:
        dict: Словарь с минимальными и максимальными значениями для price и price_for_1ton
    """
    # Получение всех значений цен из базы данных
    prices = [lot.price for lot in db.query(Lots.price).filter(Lots.price != None).all() if lot.price is not None]
    prices_per_ton = [lot.price_for_1ton for lot in db.query(Lots.price_for_1ton).filter(Lots.price_for_1ton != None).all() if lot.price_for_1ton is not None]
    
    result = {
        'price': {
            'min': None,
            'max': None,
            'avg': None
        },
        'price_for_1ton': {
            'min': None,
            'max': None,
            'avg': None
        }
    }
    
    # Если есть значения цен, вычисляем диапазоны
    if prices:
        avg_price = statistics.mean(prices)
        result['price']['min'] = avg_price * 0.5  # Минимальная цена - 50% от средней
        result['price']['max'] = avg_price * 2    # Максимальная цена - 200% от средней
        result['price']['avg'] = avg_price
    
    # Если есть значения цен за тонну, вычисляем диапазоны
    if prices_per_ton:
        avg_price_per_ton = statistics.mean(prices_per_ton)
        result['price_for_1ton']['min'] = avg_price_per_ton * 0.5  # Минимальная цена - 50% от средней
        result['price_for_1ton']['max'] = avg_price_per_ton * 2    # Максимальная цена - 200% от средней
        result['price_for_1ton']['avg'] = avg_price_per_ton
    
    return result 