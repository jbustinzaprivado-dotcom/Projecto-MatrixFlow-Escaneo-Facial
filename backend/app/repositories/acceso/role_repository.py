from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Rol


def get_by_nombre(db: Session, nombre: str) -> Rol | None:
    return db.scalar(select(Rol).where(Rol.nombre == nombre))
