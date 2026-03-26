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
