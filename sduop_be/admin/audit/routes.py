from fastapi import APIRouter, Depends, Request
from core.database import get_db
from sqlalchemy.orm import Session
from authz.current_user import get_current_user, CurrentUser
from utils.datatable_utils import DTParams
from sduop_be.admin.audit.controllers import (
    audit_events_dt_c,
    audit_event_detail_c,
    get_list_entities_c,
    get_list_actions_c
)
from sduop_be.admin.audit.schemas import AuditDTResponse, AuditDetailResponse, EntitiesDetailResponse, ActionsDetailResponse
import logging

router = APIRouter(prefix="/data_bitacora", tags=["Bitacora"])
logger = logging.getLogger("bitacora_r")


@router.post("/audit", summary="Consultar bitácora (datatable)", response_model=AuditDTResponse)
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


@router.get("/audit/event", summary="Detalle de un evento", response_model=AuditDetailResponse)
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

@router.get("/entities", summary="Obtener las entidades de la bitácora", response_model=EntitiesDetailResponse)
def get_all_entities_r(
    v: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna todas las entidades de la bitácora
    """
    logger.debug(f"[get_all_entities_r] Consultando lista de entidades, vista: {v}")
    return get_list_entities_c(v, current_user, db)

@router.get("/actions", summary="Obtener las acciones de la bitácora", response_model=ActionsDetailResponse)
def get_all_actions_r(
    v: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna todas las acciones de la bitácora
    """
    logger.debug(f"[get_all_actions_r] Consultando lista de acciones, vista: {v}")
    return get_list_actions_c(v, current_user, db)

