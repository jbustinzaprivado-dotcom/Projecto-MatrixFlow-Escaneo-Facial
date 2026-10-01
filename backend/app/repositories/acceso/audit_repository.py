from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Auditoria


def add(
    db: Session,
    *,
    usuario_id: int | None,
    accion: str,
    recurso: str,
    resultado: str,
    detalle: str | None,
    sucursal_id: int | None,
) -> Auditoria:
    entrada = Auditoria(
        usuario_id=usuario_id,
        accion=accion,
        recurso=recurso,
        resultado=resultado,
        detalle=detalle,
        sucursal_id=sucursal_id,
    )
    db.add(entrada)
    db.commit()
    db.refresh(entrada)
    return entrada


def list_all(db: Session) -> list[Auditoria]:
    return list(
        db.scalars(
            select(Auditoria)
            .options(selectinload(Auditoria.usuario), selectinload(Auditoria.sucursal))
            .order_by(Auditoria.creado_en.desc(), Auditoria.id.desc())
        )
    )
