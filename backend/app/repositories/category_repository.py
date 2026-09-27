from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Categoria


def get_or_create(db: Session, nombre: str) -> Categoria:
    categoria = db.scalar(select(Categoria).where(Categoria.nombre == nombre))
    if categoria is None:
        categoria = Categoria(nombre=nombre)
        db.add(categoria)
        db.flush()
    return categoria
