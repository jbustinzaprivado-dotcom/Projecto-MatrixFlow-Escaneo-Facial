from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Meta


def list_all(db: Session) -> list[Meta]:
    return list(db.scalars(select(Meta).order_by(Meta.periodo.desc(), Meta.id)))


def create(db: Session, *, sucursal_id: int, producto_id: int, cantidad_meta: int, periodo: str) -> Meta:
    meta = Meta(
        sucursal_id=sucursal_id, producto_id=producto_id, cantidad_meta=cantidad_meta, periodo=periodo
    )
    db.add(meta)
    db.commit()
    db.refresh(meta)
    return meta
