from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import VerificacionIntento


def add(
    db: Session, *, dni: str, usuario_id: int | None, coincide: bool, similitud: float | None
) -> VerificacionIntento:
    intento = VerificacionIntento(
        dni=dni, usuario_id=usuario_id, coincide=coincide, similitud=similitud
    )
    db.add(intento)
    db.commit()
    db.refresh(intento)
    return intento


def list_all(db: Session) -> list[VerificacionIntento]:
    return list(
        db.scalars(
            select(VerificacionIntento).order_by(
                VerificacionIntento.creado_en.desc(), VerificacionIntento.id.desc()
            )
        )
    )
