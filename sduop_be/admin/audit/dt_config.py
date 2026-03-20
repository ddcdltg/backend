from utils.datatable_utils import DTConfig
from bitacora.models import AuditAdmin

# Mapa de tablas por módulo — agrega aquí cada módulo que quieras auditar
AUDIT_TABLE_MAP = {
    "users":        "audit_users",
    "roles":        "audit_roles",
    "permisos":     "audit_permisos",
    "estatus":      "audit_estatus",
    "audit_*":      "audit_log",   # fallback / vista global
}

GLOBAL_BITACORA_CFG = DTConfig(
    pk_col=AuditAdmin.event_id,
    orderable_map={
        "audit_id":    AuditAdmin.audit_id,
        "event_id":    AuditAdmin.event_id,
        "created_at":  AuditAdmin.created_at,
        "actor_id":    AuditAdmin.actor_id,
        "action":      AuditAdmin.action,
        "table_name":  AuditAdmin.table_name,
        "record_id":   AuditAdmin.record_id,
        "ip_address":  AuditAdmin.ip_address,
        "view_id":     AuditAdmin.view_id,
    },
    searchable_cols=[
        AuditAdmin.event_id,
        AuditAdmin.action,
        AuditAdmin.table_name,
        AuditAdmin.actor_id,
        AuditAdmin.ip_address,
    ],
    default_order_col=AuditAdmin.created_at,
)


