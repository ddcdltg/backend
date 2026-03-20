from sqlalchemy.orm import Session
from authz.current_user import CurrentUser
from utils.datatable_utils import  DTParams
from typing import List, Dict, Any
from sduop_be.admin.authz_status.services import get_all_status_s
from authz.filters.auth import get_auth
from sduop_be.admin.authz_status.dt_config import STATUS_DT_CFG
import logging
from starlette.status import HTTP_200_OK

logger = logging.getLogger("status_c")
STATUS_RESOURCE = "Estatus"
READ = "Consultar"

def get_all_status_c(
        *,
        view_id: int, 
        dt_params: DTParams,               
        current_user:CurrentUser, 
        db: Session
) -> List[Dict[str, Any]]:
    case, resource_id= get_auth(
        db=db,
        current_user=current_user,
        view_id=view_id,
        obj_prefix=STATUS_RESOURCE,
        action=READ
    )
    
    result = get_all_status_s(
        case=case, 
        view_id=view_id,
        resource_id=resource_id,
        current_user=current_user, 
        db=db,
        dt_params=dt_params,        
        dt_cfg=STATUS_DT_CFG
    ) 

    logger.debug("get_all_status_c → result=%r", result)
    return {
    "httpCode": HTTP_200_OK,
    "error_message": "",
    "message": "Registros recuperados correctamente",
    "response": result
}