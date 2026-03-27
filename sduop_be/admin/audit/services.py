from sqlalchemy.orm import Session
from authz.current_user import CurrentUser
from utils.datatable_utils import DTParams, DTConfig, apply_datatable_pipeline
from typing import Optional, List, Dict, Any, Union
from bitacora.models import AuditAdmin
from sduop_be.admin.audit.crud import get_list_entities_db, get_list_actions_db, get_list_records_db
from sduop_be.admin.audit.utils import serialize_audit_records, serialize_audit_detail
import logging

logger = logging.getLogger("bitacora_s")


def _build_base_query(db: Session, filters: dict):
    """Query base con todos los filtros opcionales aplicados."""
    q = db.query(AuditAdmin)

    if filters.get("action"):
        q = q.filter(AuditAdmin.action == filters["action"])
    if filters.get("actor_id"):
        q = q.filter(AuditAdmin.actor_id == int(filters["actor_id"]))
    if filters.get("record_id"):
        q = q.filter(AuditAdmin.record_id == int(filters["record_id"]))
    if filters.get("ip"):
        q = q.filter(AuditAdmin.ip_address == filters["ip"])
    if filters.get("table_name"):
        q = q.filter(AuditAdmin.table_name == filters["table_name"])
    if filters.get("event_id"):
        q = q.filter(AuditAdmin.event_id == filters["event_id"])
    if filters.get("date_from"):
        q = q.filter(AuditAdmin.created_at >= filters["date_from"])
    if filters.get("date_to"):
        q = q.filter(AuditAdmin.created_at <= filters["date_to"])

    return q


def audit_events_dt_s(
    *,
    case: int,
    view_id: int,
    params: dict,
    resource_id: int,
    current_user: CurrentUser,
    db: Session,
    dt_params: Optional[DTParams] = None,
    dt_cfg: Optional[DTConfig] = None,
    
) -> Union[List[Dict], Dict[str, Any]]:
    
    module = (params.get("module") or "").strip() or "audit_*"

    raw_filters = params.get("filters", {})

    filters = {
        "action":     raw_filters.get("action"),
        "actor_id":   raw_filters.get("actor_id"),
        "record_id":  raw_filters.get("record_id"),
        "ip":         raw_filters.get("ip"),
        "date_from":  raw_filters.get("date_from"),
        "date_to":    raw_filters.get("date_to"),
        "event_id":   raw_filters.get("event_id"),
        "table_name": raw_filters.get("table_name"),
    }

    logger.warning("PARAMS: %s", params)
    logger.warning("RAW FILTERS: %s", raw_filters)
    logger.warning("FILTERS: %s", filters)

    # Si el módulo es específico filtra por table_name
    if module and module != "audit_*":
        filters["table_name"] = module

    if case == 1:  # ADMIN — ve todo
        base = _build_base_query(db, filters)
    else:
        raise ValueError(f"case no válido: {case}")

    logger.debug("=====> base query: %s", base)

    if dt_params and dt_cfg:
        return apply_datatable_pipeline(
            base_q=base,
            case=case,
            current_user=current_user,
            db=db,
            dt_params=dt_params,
            dt_cfg=dt_cfg,
            id_col=AuditAdmin.audit_id,
            view_id=view_id,
            resource_id=resource_id,
            serialize_fn=serialize_audit_records,
        )
    return []


def audit_event_detail_s(
    *,
    db: Session,
    event_id: str,
) -> List[Dict]:
    """Devuelve todos los campos cambiados para un event_id."""
    rows = (
        db.query(AuditAdmin)
        .filter(AuditAdmin.event_id == event_id)
        .order_by(AuditAdmin.audit_id)
        .all()
    )
    return serialize_audit_detail(rows)

def audit_modules_s(*, db: Session) -> List[str]:
    """Distinct de table_name — para el dropdown de módulos."""
    rows = (
        db.query(AuditAdmin.table_name)
        .distinct()
        .order_by(AuditAdmin.table_name)
        .all()
    )
    return [r.table_name for r in rows]


def audit_actions_s(*, db: Session) -> List[str]:
    """Distinct de action — insert, update, delete, read, error."""
    rows = (
        db.query(AuditAdmin.action)
        .distinct()
        .order_by(AuditAdmin.action)
        .all()
    )
    return [r.action for r in rows]


def audit_actors_s(*, db: Session) -> List[int]:
    """Distinct de actor_id — para el dropdown de usuarios."""
    rows = (
        db.query(AuditAdmin.actor_id)
        .filter(AuditAdmin.actor_id.isnot(None))
        .distinct()
        .order_by(AuditAdmin.actor_id)
        .all()
    )
    return [r.actor_id for r in rows]


def get_list_entities_s(*, db: Session): 
    result = get_list_entities_db(db)

    return result

def get_list_actions_s(*, db: Session): 
    result = get_list_actions_db(db)

    return result

def get_list_records_s(*,entity: str, db: Session): 
    result = get_list_records_db(entity, db)

    return result