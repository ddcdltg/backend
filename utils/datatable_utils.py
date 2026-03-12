# Reutilizable para cualquier entidad
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from sqlalchemy.sql.elements import ColumnElement, UnaryExpression
from sqlalchemy.sql.selectable import Select
import logging, time
logger = logging.getLogger("datatable_u")
 


@dataclass(frozen=True)
class DTConfig:
    pk_col: ColumnElement
    orderable_map: Dict[str, ColumnElement | UnaryExpression]
    searchable_cols: List[ColumnElement]
    default_order_col: ColumnElement


class DTParams:
    def __init__(self, params: Dict[str, Any]) -> None:
        def get_nested(obj, path, default=None):
            cur = obj
            for key in path:
                if isinstance(key, int):
                    if isinstance(cur, list) and 0 <= key < len(cur):
                        cur = cur[key]
                    else:
                        return default
                else:
                    if isinstance(cur, dict):
                        cur = cur.get(key, default)
                    else:
                        return default
            return cur

        # draw, start, length
        self.draw   = int(params.get("draw", 1) or 1)
        self.start  = max(int(params.get("start", 0) or 0), 0)
        self.length = min(max(int(params.get("length", 10) or 10), 1), 100)

        # search: JSON -> search.value ; plano -> "search[value]"
        sv = get_nested(params, ["search", "value"], None)
        if sv is None:
            sv = params.get("search[value]", "")
        self.search = (sv or "").strip()

        # order index: JSON -> order[0].column ; plano -> "order[0][column]"
        idx = get_nested(params, ["order", 0, "column"], None)
        if idx is None:
            idx = params.get("order[0][column]", 0)
        try:
            idx = int(idx)
        except (TypeError, ValueError):
            idx = 0

        # order dir: JSON -> order[0].dir ; plano -> "order[0][dir]"
        self.order_dir = (
            get_nested(params, ["order", 0, "dir"], None)
            or params.get("order[0][dir]", "asc")
            or "asc"
        ).lower()

        # column data name: JSON -> columns[idx].data ; plano -> "columns[idx][data]"
        col_data = None
        cols = params.get("columns")
        if isinstance(cols, list) and 0 <= idx < len(cols):
            col_data = cols[idx].get("data")
        if col_data is None:
            col_data = params.get(f"columns[{idx}][data]", None)
        self.order_name = col_data


def dt_apply_search(q: Select, search: str, cfg: DTConfig) -> Select:
    if not search:
        return q
    like = f"%{search}%"
    ors = [col.ilike(like) for col in cfg.searchable_cols]
    # SQLAlchemy construye los OR con el operador |
    cond = None
    for c in ors:
        cond = c if cond is None else (cond | c)
    return q.filter(cond) if cond is not None else q


def dt_apply_order(q: Select, order_name: Optional[str], order_dir: str, cfg: DTConfig) -> Select:
    col = cfg.orderable_map.get(order_name, cfg.default_order_col)
    ordering = asc(col) if order_dir == "asc" else desc(col)
    return q.order_by(ordering)


def dt_execute(db: Session, q_auth: Select, dt: DTParams, cfg: DTConfig) -> Tuple[int, int, List[Any]]:
    """
    Ejecuta conteos y trae SOLO la página (genérico).
    - records_total: total del universo autorizado sin search
    - records_filtered: con search
    - rows: filas de la página (ORM rows/tupla)
    """
    records_total = db.query(func.count(cfg.pk_col)).select_from(q_auth.subquery()).scalar()

    q_filtered = dt_apply_search(q_auth, dt.search, cfg)
    records_filtered = db.query(func.count(cfg.pk_col)).select_from(q_filtered.subquery()).scalar()

    q_ordered = dt_apply_order(q_filtered, dt.order_name, dt.order_dir, cfg)
    rows = q_ordered.offset(dt.start).limit(dt.length).all()
    return records_total, records_filtered, rows


def dt_build_payload(draw: int, total: int, filtered: int, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": filtered,
        "data": data,
    }


def apply_datatable_pipeline(
    *,
    base_q,
    case: int,
    current_user,
    db: Session,
    dt_params: DTParams,
    dt_cfg: DTConfig,
    id_col: ColumnElement,
    view_id: int,
    resource_id: int,
    serialize_fn,
    return_dt_payload: bool = True,
):
    t0 = time.perf_counter()

    # ==========================
    # Filtro de búsqueda
    # ==========================
    q_filtered = base_q   # inicialización segura

    if dt_params.search:
        like = f"%{dt_params.search}%"
        cond = None
        for col in dt_cfg.searchable_cols:
            c = col.ilike(like)
            cond = c if cond is None else (cond | c)
        if cond is not None:
            q_filtered = q_filtered.filter(cond)

    # ==========================
    # Conteos (total + filtrado)
    # ==========================
    t1 = time.perf_counter()

    # Para evitar el problema de duplicados por JOIN usamos distinct sobre la PK
    # Esto es clave para no inflar ni hacer COUNT costoso
    total_subq = base_q.with_entities(func.distinct(id_col).label("id")).subquery()
    filtered_subq = q_filtered.with_entities(func.distinct(id_col).label("id")).subquery()

    records_total = db.query(func.count()).select_from(total_subq).scalar()
    records_filtered = db.query(func.count()).select_from(filtered_subq).scalar()

    t2 = time.perf_counter()
    logger.debug(
        "[DT] counts total+filtered=%.2f ms (total=%d, filtered=%d)",
        (t2 - t1) * 1000, records_total, records_filtered
    )

    # ==========================
    # Query de página
    # ==========================
    t3 = time.perf_counter()
    rows = (
        q_filtered
        .order_by(
            asc(dt_cfg.orderable_map.get(dt_params.order_name, dt_cfg.default_order_col))
            if dt_params.order_dir == "asc"
            else desc(dt_cfg.orderable_map.get(dt_params.order_name, dt_cfg.default_order_col))
        )
        .offset(dt_params.start)
        .limit(dt_params.length)
        .all()
    )
    t4 = time.perf_counter()
    logger.debug("[DT] fetch rows=%.2f ms (n=%d)", (t4 - t3) * 1000, len(rows))

    # ==========================
    # Serialización (optimizada con batch)
    # ==========================
    t5 = time.perf_counter()
    page = serialize_fn(rows, view_id, resource_id, case, db, current_user)
    t6 = time.perf_counter()
    logger.debug("[DT] serialize_fn=%.2f ms", (t6 - t5) * 1000)

    # ==========================
    # Pipeline total
    # ==========================
    t7 = time.perf_counter()
    logger.debug("[DT] total pipeline=%.2f ms", (t7 - t0) * 1000)

    # ==========================
    # Construcción payload
    # ==========================
    payload = dt_build_payload(
        draw=dt_params.draw,
        total=records_total,
        filtered=records_filtered,
        data=page,
    )
    return payload if return_dt_payload else page