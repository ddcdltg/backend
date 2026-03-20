from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AuditTable(BaseModel):

    event_id: str
    created_at: datetime
    actor_id: int
    view_id: int
    ip_address: str
    action: str
    table_name: str
    record_id: int
    changes_count: Optional[int] = None
    field_name: Optional[str] = None
    value: Optional[str] = None
    meta: Optional[str] = None
    audit_source: str | None = None

    class Config:
        from_attributes = True
        extra = "forbid"