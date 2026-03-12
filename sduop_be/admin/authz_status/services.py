from utils.datatable_utils import  DTParams
from sqlalchemy.orm import Session
from authz.current_user import CurrentUser
from utils.datatable_utils import  DTParams, DTConfig, apply_datatable_pipeline
from typing import List, Dict, Any, Optional, Union
from sduop_be.admin.authz_status.crud import get_all_status_db, table_is_empty
from bitacora.models import Status
from sduop_be.admin.authz_status.utils import serialize_status_records
import logging

logger = logging.getLogger("status_s")

STATUS_ID = "status_id"
STATUS_RESOURCE = "Estatus"
READ = "Consultar"

def get_all_status_s(
        *, 
        case: int, 
        view_id: int,
        resource_id=int,
        current_user: CurrentUser, 
        db: Session,
        dt_params: Optional[DTParams] = None,
        dt_cfg: Optional[DTConfig] = None
) -> Union[List[Dict], Dict[str, Any]]:
    
    # A) prepara subjects una sola vez (se usa en case 2 y 3)
    #subjects = build_subjects(current_user.user_id, current_user.unit_id)
    
    # B) Selección base por case  
    
    #if case == 3:
    
    #Case 1: ADMIN
    if case == 1:
        base = get_all_status_db(db)

    #elif case == 2:
        # RBAC general: aplica deny-override en SQL (una sola query)
       
    else:
        raise ValueError(f"case no válido: {case}")
        
    if table_is_empty(db, Status):
        logger.debug("[get_all_status_s] Tabla Status vacía")

    logger.debug("=====>base: %s", base)
    if dt_params and dt_cfg:
        return apply_datatable_pipeline(
                base_q=base,
                case=case,
                current_user=current_user,
                db=db,
                dt_params=dt_params,
                dt_cfg=dt_cfg,
                id_col=Status.status_id,
                view_id=view_id,
                resource_id=resource_id,
                serialize_fn=serialize_status_records
        )