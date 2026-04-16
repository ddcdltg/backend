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
    audit_source: Optional[str] = None

    class Config:
        from_attributes = True
        extra = "forbid"


class AuditLogOut(BaseModel):
    """Un renglón del datatable (vista agrupada por evento)."""
    audit_id:      int
    event_id:      str
    created_at:    datetime
    actor_id:      int
    view_id:       int
    ip_address:    Optional[str] = None
    action:        str
    table_name:    str
    record_id:     Optional[int] = None
    changes_count: Optional[int] = None
    meta:          Optional[str] = None
    audit_source:  Optional[str] = None
    permissions:   Optional[list[str]] = None

    class Config:
        from_attributes = True
        extra = "forbid"


class AuditLogDetailOut(BaseModel):
    """Un renglón del detalle (field_name / value por evento)."""
    audit_id:   int
    field_name: Optional[str] = None
    value:      Optional[str] = None

    class Config:
        from_attributes = True
        extra = "forbid"


class DataTableOut(BaseModel):
    draw:            int
    recordsTotal:    int
    recordsFiltered: int
    data:            List[AuditLogOut]


class AuditDTResponse(BaseModel):
    httpCode:      int
    error_message: str
    message:       str
    response:      DataTableOut


class AuditDetailResponse(BaseModel):
    httpCode:      int
    error_message: str
    message:       str
    response:      List[AuditLogDetailOut]

class EntitiesPartialOut(BaseModel):
    entity_id: str
    name: str

    class Config:
        from_attributes = True
        extra = "forbid"

class EntitiesDetailResponse(BaseModel):
    httpCode:      int
    error_message: str
    message:       str
    response:      List[EntitiesPartialOut]

class ActionsPartialOut(BaseModel):
    action_id: str
    name: str

    class Config:
        from_attributes = True
        extra = "forbid"

class ActionsDetailResponse(BaseModel):
    httpCode:      int
    error_message: str
    message:       str
    response:      List[ActionsPartialOut]

class RecordsPartialOut(BaseModel):
    record_id: str

    class Config:
        from_attributes = True
        extra = "forbid"

class RecordsDetailResponse(BaseModel):
    httpCode:      int
    error_message: str
    message:       str
    response:      List[RecordsPartialOut]