from sqlalchemy.orm import Session
from logging import getLogger
from authz.current_user import CurrentUser

logger = getLogger("auth")

from typing import NamedTuple

class AuthCase(NamedTuple):
    case: int
    resource_id: int
    
def get_auth(
    *,
    db: Session,
    current_user: CurrentUser,
    view_id: int,
    obj_prefix: str,
    action: str
) -> AuthCase:
    logger.info("[MOCK get_auth] Retornando siempre GLOBAL_ADMIN")
    return 1, view_id