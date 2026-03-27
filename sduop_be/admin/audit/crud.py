from sqlalchemy.orm import Session
from bitacora.models import AuditAdmin
import logging

logger = logging.getLogger("bitacora_db")

def get_list_entities_db(db: Session):
    try:
        rows = (
            db.query(AuditAdmin.table_name.label("name"))
            .distinct()
            .all()
        )

        logger.debug(f"Consultando lista de entidades: {rows}")

        return [
            {
                "entity_id": row.name,
                "name": row.name
            }
            for row in rows
        ]

    except Exception as e:
        logger.error(f"Error obteniendo entidades: {e}")
        return []
    
def get_list_actions_db(db: Session):
    try:
        rows = (
            db.query(AuditAdmin.action.label("action"))
            .distinct()
            .all()
        )

        logger.debug(f"Consultando lista de acciones: {rows}")

        return [
            {
                "action_id": row.action,
                "name": row.action
            }
            for row in rows
        ]

    except Exception as e:
        logger.error(f"Error obteniendo acciones: {e}")
        return []
    
def get_list_records_db(entity:str, db: Session):
    try:
        rows = (
            db.query(AuditAdmin.record_id.label("record_id"))
            .filter(AuditAdmin.table_name==entity)
            .distinct()
            .all()
        )

        logger.debug(f"Consultando lista de id de registros: {rows}")

        return [
            {
                "record_id": row.record_id,
            }
            for row in rows
        ]

    except Exception as e:
        logger.error(f"Error obteniendo registros: {e}")
        return []
