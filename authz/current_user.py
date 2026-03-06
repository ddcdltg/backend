from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import get_db
from logging import getLogger
from pydantic import BaseModel
from typing import List

logger = getLogger("current_user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class CurrentUser(BaseModel):
    user_id: int
    user_guid: str
    full_name: str
    profiles: List[int]
    unit_id: int

    class Config:
        from_attributes = True
        extra = "forbid"

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> CurrentUser:
    """
    Función simulada para desarrollo/pruebas.
    No hace validaciones reales, no consulta BD y no realiza peticiones externas.
    Cualquier token recibido se considera válido.
    """

    logger.debug(f"[get_current_user MOCK] Token recibido: {token}")

    current_user = CurrentUser(
        user_id=1,
        user_guid="mock-guid-123456",
        full_name="Usuario Simulado",
        profiles=[1, 2],   # IDs de perfiles simulados
        unit_id=10
    )

    logger.debug(
        f"[get_current_user MOCK] Datos completos: "
        f"{current_user.dict() if hasattr(current_user, 'dict') else current_user}"
    )
    logger.info("[MOCK] Sesión simulada válida")

    return current_user