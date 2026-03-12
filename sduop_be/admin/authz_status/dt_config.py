from sqlalchemy import func
from bitacora.models import Status
from utils.datatable_utils import DTConfig


STATUS_DT_CFG = DTConfig(
    pk_col=Status.status_id,
    orderable_map={
        "id": Status.status_id,
        "name": Status.status_name,
        "description": Status.status_description
    },
    searchable_cols=[Status.status_name, Status.status_description, Status.status_id],
    default_order_col=Status.status_id,
)