from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from pydantic import BaseModel

from app.repositories.models import Base
from app.core.exception_handlers import NotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        result = db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    def get_or_404(self, db: Session, id: Any, error_msg: str = None) -> ModelType:
        obj = self.get(db, id)
        if not obj:
            if not error_msg:
                error_msg = f"{self.model.__name__} с id={id} не найден"
            raise NotFoundException(message=error_msg)
        return obj

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    def get_by_attribute(
        self, db: Session, attr_name: str, attr_value: Any
    ) -> Optional[ModelType]:
        result = db.execute(
            select(self.model).filter(getattr(self.model, attr_name) == attr_value)
        )
        return result.scalars().first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = self.get_or_404(db, id)
        db.delete(obj)
        db.commit()
        return obj 