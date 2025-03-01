from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Lots(Base):
    __tablename__ = "lots"

    number = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=True, server_default=func.now())
    code_KSSS_NB = Column(Integer, nullable=True)
    code_KSSS_fuel = Column(Integer, nullable=True)
    start_weight = Column(Integer, nullable=True)
    current_weight = Column(Integer, nullable=True, default=start_weight)
    status = Column(String, nullable=True, default='Подтвержден')
    price = Column(Integer, nullable=True)
    price_for_1ton = Column(Integer, nullable=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    order_date = Column(DateTime, nullable=True, server_default=func.now())
    lot_number = Column(Integer, nullable=True)
    code_KSSS_NB = Column(Integer, nullable=True)
    code_KSSS_fuel = Column(Integer, nullable=True)
    volume = Column(Integer, nullable=True)
    delivery_type = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
