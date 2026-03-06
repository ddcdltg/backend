from sqlalchemy.orm import Session
from authz.current_user import CurrentUser
from typing import List, Optional
from sduop_be.admin.authz_status.schemas import StatusOut
import logging

logger = logging.getLogger("status_s")


def serialize_status_records(
    rows: list, 
    view_id: int,
    resource_id:int,
    case: int,
    db: Session,
    current_user: Optional[CurrentUser] = None,
) -> List[StatusOut]:

    out = []

    permissions_map = {}
    if current_user and case != 1:
        ids = [r.status_id for r in rows]
        permissions_map = ["*"]
    for r in rows:
        item = {
            "status_id": r.status_id,
            "name": r.status_name,
            "description": r.status_description
        }
        if current_user is not None:
            if case == 1:
                item["permissions"] = ["*"]#resource_actions[:]   # todas
            else:
                item["permissions"] = permissions_map.get(r.status_id, [])
        out.append(item)
    return out