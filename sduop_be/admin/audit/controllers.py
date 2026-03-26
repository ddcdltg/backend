from sqlalchemy.orm import Session
from authz.current_user import CurrentUser
from authz.filters.auth import get_auth
from utils.datatable_utils import DTParams
from sduop_be.admin.audit.services import audit_events_dt_s, audit_event_detail_s, get_list_entities_s
from sduop_be.admin.audit.dt_config import GLOBAL_BITACORA_CFG, AUDIT_TABLE_MAP
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import logging
from sduop_be.admin.audit.schemas import EntitiesPartialOut

logger = logging.getLogger("bitacora_c")

# Constantes locales del módulo
AUDIT_RESOURCE = "Bitácora"
READ = "Consultar"


def audit_events_dt_c(
    *,
    view_id: int,
    params: dict,
    dt_params: DTParams,
    current_user: CurrentUser,
    db: Session,
) -> dict:
    # autorización
    case, resource_id = get_auth(
        db=db,
        current_user=current_user,
        view_id=view_id,
        obj_prefix=AUDIT_RESOURCE,
        action=READ,
    )

    result = audit_events_dt_s(
        case=case,
        view_id=view_id,
        params = params,
        resource_id=resource_id,
        current_user=current_user,
        db=db,
        dt_params=dt_params,
        dt_cfg=GLOBAL_BITACORA_CFG,
    )

    logger.debug("audit_events_dt_c → result=%r", result)
    return {
        "httpCode":      HTTP_200_OK,
        "error_message": "",
        "message":       "Bitácora obtenida correctamente",
        "response":      result,
    }


def audit_event_detail_c(
    *,
    view_id: int,
    event_id: str,
    module: str,
    current_user: CurrentUser,
    db: Session,
) -> dict:
    module = (module or "").strip()

    if not module:
        return {
            "httpCode":      HTTP_400_BAD_REQUEST,
            "error_message": "module requerido",
            "message":       "module requerido",
            "response":      [],
        }

    if module not in AUDIT_TABLE_MAP:
        return {
            "httpCode":      HTTP_400_BAD_REQUEST,
            "error_message": "module inválido",
            "message":       "module inválido",
            "response":      [],
        }

    case, resource_id = get_auth(
        db=db,
        current_user=current_user,
        view_id=view_id,
        obj_prefix=AUDIT_RESOURCE,
        action=READ,
    )

    rows = audit_event_detail_s(
        db=db,
        event_id=event_id,
    )

    return {
        "httpCode":      HTTP_200_OK,
        "error_message": "",
        "message":       "Detalle de evento obtenido correctamente",
        "response":      rows,
    }

def get_list_entities_c(view_id: int, current_user, db: Session):
    
    case, resource_id = get_auth(
        db=db,
        current_user=current_user,
        view_id=view_id,
        obj_prefix=AUDIT_RESOURCE,
        action=READ,
    )
 
    obj_list = get_list_entities_s(db=db)
    logger.debug("[get_list_entities_c] obj_list=%s", obj_list)
    result = [EntitiesPartialOut.model_validate({"entity_id": r[0], "name": r[1]}) for r in obj_list]

    return {
        "httpCode":      HTTP_200_OK,
        "error_message": "",
        "message":       "Entidades obtenidas correctamente",
        "response":      result,
    }
