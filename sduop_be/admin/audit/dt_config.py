from utils.datatable_utils import DTConfig
from bitacora.models import AuditLog


# Mapa de tablas por módulo — agrega aquí cada módulo que quieras auditar
AUDIT_TABLE_MAP = {
    "users":        "audit_users",
    "roles":        "audit_roles",
    "permisos":     "audit_permisos",
    "estatus":      "audit_estatus",
    "audit_*":      "audit_log",   # fallback / vista global
}

GLOBAL_BITACORA_CFG = DTConfig(
    pk_col=AuditLog.event_id,
    orderable_map={
        "event_id":    AuditLog.event_id,
        "created_at":  AuditLog.created_at,
        "actor_id":    AuditLog.actor_id,
        "action":      AuditLog.action,
        "table_name":  AuditLog.table_name,
        "record_id":   AuditLog.record_id,
        "ip_address":  AuditLog.ip_address,
        "view_id":     AuditLog.view_id,
    },
    searchable_cols=[
        AuditLog.event_id,
        AuditLog.action,
        AuditLog.table_name,
        AuditLog.actor_id,
        AuditLog.ip_address,
    ],
    default_order_col=AuditLog.created_at,
    audit_table_map=AUDIT_TABLE_MAP,   # <-- campo extra para validar módulos
)

from utils.datatable_utils import DTConfig
from bitacora.models import AuditAdmin

# Separado del DTConfig porque el dataclass no acepta campos extra
AUDIT_TABLE_MAP = {
    "users":   "audit_admin",
    "roles":   "audit_admin",
    "estatus": "audit_admin",
    "audit_*": "audit_admin",  # fallback global
}

