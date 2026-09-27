from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.types import utcnow
from app.models import Inventario, MovimientoInventario


def list_all(db: Session) -> list[Inventario]:
    return list(db.scalars(select(Inventario).order_by(Inventario.id)))


def get_by_sucursal_producto(db: Session, sucursal_id: int, producto_id: int) -> Inventario | None:
    return db.scalar(
        select(Inventario).where(
            Inventario.sucursal_id == sucursal_id, Inventario.producto_id == producto_id
        )
    )


def get_or_create(db: Session, sucursal_id: int, producto_id: int) -> Inventario:
    inventario = get_by_sucursal_producto(db, sucursal_id, producto_id)
    if inventario is not None:
        return inventario
    inventario = Inventario(sucursal_id=sucursal_id, producto_id=producto_id, existencias=0)
    db.add(inventario)
    db.commit()
    db.refresh(inventario)
    return inventario


def add_movimiento(
    db: Session, *, inventario_id: int, tipo: str, cantidad: int
) -> MovimientoInventario:
    movimiento = MovimientoInventario(inventario_id=inventario_id, tipo=tipo, cantidad=cantidad)
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento


def ajustar_existencias(db: Session, inventario: Inventario, delta: int) -> Inventario:
    inventario.existencias += delta
    inventario.actualizado_en = utcnow()
    db.commit()
    db.refresh(inventario)
    return inventario
