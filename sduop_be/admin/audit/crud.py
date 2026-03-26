from sqlalchemy.orm import Session
from sqlalchemy import distinct
from bitacora.models import AuditAdmin 


def get_list_entities_db(db: Session):
    try:
        result = (
            db.query(distinct(AuditAdmin.table_name.label("name")))
            .all()
        )

        # Convertir de lista de tuplas a lista simple
        entities = [row[0] for row in result]

        return entities

    except Exception as e:
        print(f"Error al obtener entidades: {e}")
        return []
