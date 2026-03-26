from sqlalchemy.orm import Session
from sqlalchemy import distinct
from bitacora.models import AuditAdmin 


def get_list_entities_db(db: Session):
    try:
        rows = (
            db.query(distinct(AuditAdmin.table_name.label("name")))
            .all()
        )

    
        return [
            {
                "entity_id": row.name,
                "name": row.name
            }
            for row in rows
        ]

    except Exception as e:
        print(f"Error al obtener entidades: {e}")
        return []
