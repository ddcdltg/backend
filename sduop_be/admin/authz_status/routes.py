from fastapi import APIRouter, Depends, Request 
from sduop_be.admin.authz_status.schemas import StatusResponse
from core.database import get_db
from sqlalchemy.orm import Session
from authz.current_user import get_current_user
from utils.datatable_utils import  DTParams
from sduop_be.admin.authz_status.controllers import get_all_status_c
import logging

router = APIRouter() #importar librería
logger = logging.getLogger("status_r")

#@router llama a la api, .post es el método, url para llegar al backend, summary es para testing, response model se pone siempre
@router.post("/status", summary="Obtener todos los estatus (datatable)", response_model=StatusResponse)
async def get_all_status_r(
    v: int,
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)  
):
    
    
    logger.debug(f"[get_all_status_r] Consultando estatus, vista: {v}")

    params = await request.json() 
    dt_params = DTParams(params)

    return get_all_status_c(
            view_id=v,
            dt_params=dt_params,
            current_user=current_user,
            db=db
        )