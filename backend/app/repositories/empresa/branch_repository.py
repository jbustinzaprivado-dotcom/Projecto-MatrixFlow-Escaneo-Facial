from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Sucursal


def list_all(db: Session) -> list[Sucursal]:
    return list(db.scalars(select(Sucursal).order_by(Sucursal.id)))


def get(db: Session, sucursal_id: int) -> Sucursal | None:
    return db.get(Sucursal, sucursal_id)


def create(db: Session, *, company_id: int, nombre: str, departamento: str, distrito: str, direccion: str) -> Sucursal:
    sucursal = Sucursal(
        company_id=company_id,
        nombre=nombre,
        departamento=departamento,
        distrito=distrito,
        direccion=direccion,
    )
    db.add(sucursal)
    db.commit()
    db.refresh(sucursal)
    return sucursal
