from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Producto


def list_all(db: Session) -> list[Producto]:
    return list(
        db.scalars(select(Producto).options(selectinload(Producto.categoria)).order_by(Producto.id))
    )


def get(db: Session, producto_id: int) -> Producto | None:
    return db.get(Producto, producto_id)


def create(db: Session, *, nombre: str, categoria_id: int, precio: float) -> Producto:
    producto = Producto(nombre=nombre, categoria_id=categoria_id, precio=precio)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto
