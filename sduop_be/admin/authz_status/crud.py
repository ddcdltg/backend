from sqlalchemy.orm import Session
from bitacora.models import Status
from typing import Type, Any
import logging

logger = logging.getLogger("status_db")

def get_all_status_db(db: Session):
    return db.query(Status)

def table_is_empty(db: Session, model: Type[Any]) -> bool:
    # .first() con .limit(1) evita COUNT(*) y es lo más barato
    return db.query(model).limit(1).first() is None