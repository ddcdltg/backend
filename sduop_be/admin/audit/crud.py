from sqlalchemy.orm import Session
from sqlalchemy import distinct
from bitacora.models import AuditAdmin 
import logging
logger = logging.getLogger("bitacora_db")

def get_list_entities_db(db: Session):
    try:
        rows = (
            db.query(distinct(AuditAdmin.table_name.label("name")))
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

        return []
