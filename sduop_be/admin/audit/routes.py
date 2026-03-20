from fastapi import APIRouter, Depends, Request
from core.database import get_db
from sqlalchemy.orm import Session
from authz.current_user import get_current_user, CurrentUser
from utils.datatable_utils import DTParams
from sduop_be.admin.audit.controllers import (
    audit_events_dt_c,
    audit_event_detail_c,
    audit_modules_c,
    audit_actions_c,
    audit_actors_c,
)
from sduop_be.admin.audit.schemas import AuditTable, AuditDetailResponse, AuditCatalogResponse
import logging

router = APIRouter(prefix="/data_bitacora", tags=["Bitacora"])
logger = logging.getLogger("bitacora_r")


@router.post("/audit", summary="Consultar bitácora (datatable)", response_model=AuditTable)
async def audit_events_dt_r(
    v: int,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    params = await request.json()
    dt_params = DTParams(params)
    logger.debug(f"[audit_events_dt_r] vista: {v}, params: {params}")
    return audit_events_dt_c(
        view_id=v,
        params=params,
        dt_params=dt_params,
        current_user=current_user,
        db=db,
    )


@router.get("/audit/event/{event_id}", summary="Detalle de un evento", response_model=AuditDetailResponse)
async def audit_event_detail_r(
    event_id: str,
    v: int,
    module: str = "audit_*",
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.debug(f"[audit_event_detail_r] event_id: {event_id}, module: {module}")
    return audit_event_detail_c(
        view_id=v,
        event_id=event_id,
        module=module,
        current_user=current_user,
        db=db,
    )


@router.get("/audit/modules", summary="Listado de módulos (table_name distinct)")
async def audit_modules_r(
    v: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return audit_modules_c(view_id=v, current_user=current_user, db=db)


@router.get("/audit/actions", summary="Listado de acciones (action distinct)")
async def audit_actions_r(
    v: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return audit_actions_c(view_id=v, current_user=current_user, db=db)


@router.get("/audit/actors", summary="Listado de actores (actor_id distinct)")
async def audit_actors_r(
    v: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return audit_actors_c(view_id=v, current_user=current_user, db=db)