from sqlalchemy.orm import Session

from app.models import Meta
from app.repositories.operacion import target_repository
from app.schemas.operacion.target_schema import MetaCreate


def list_metas(db: Session) -> list[Meta]:
    return target_repository.list_all(db)


def create_meta(db: Session, data: MetaCreate) -> Meta:
    return target_repository.create(
        db,
        sucursal_id=data.sucursal_id,
        producto_id=data.producto_id,
        cantidad_meta=data.cantidad_meta,
        periodo=data.periodo,
    )
