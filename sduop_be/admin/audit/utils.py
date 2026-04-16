from sqlalchemy.orm import Session
from authz.current_user import CurrentUser
from typing import List, Optional
import logging

logger = logging.getLogger("bitacora_u")


def serialize_audit_records(
    rows: list,
    view_id: int,
    resource_id: int,
    case: int,
    db: Session,
    current_user: Optional[CurrentUser] = None,
) -> List[dict]:
    """Serializa los registros para el datatable principal."""
    out = []
    for r in rows:
        item = {
            "audit_id":   r.audit_id,
            "event_id":   r.event_id,
            "created_at": r.created_at,
            "actor_id":   r.actor_id,
            "view_id":    r.view_id,
            "ip_address": r.ip_address,
            "action":     r.action,
            "table_name": r.table_name,
            "record_id":  r.record_id,
            "meta":       r.meta,
        }
        if current_user is not None:
            item["permissions"] = ["*"] if case == 1 else []
        out.append(item)
    return out


def serialize_audit_detail(rows: list) -> List[dict]:
    """Serializa el detalle campo-a-campo de un evento específico."""
    return [
        {
            "audit_id":   r.audit_id,
            "field_name": r.field_name,
            "value":      r.value,
        }
        for r in rows
    ]