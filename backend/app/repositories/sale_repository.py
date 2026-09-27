from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Producto, Sucursal, Venta, VentaDetalle


def list_all(db: Session) -> list[tuple[Venta, VentaDetalle]]:
    """Cada fila del API es una cabecera con su única línea (así se creó hasta ahora)."""
    rows = db.execute(
        select(Venta, VentaDetalle).join(VentaDetalle).order_by(Venta.id)
    ).all()
    return [(venta, detalle) for venta, detalle in rows]


def get_sucursal(db: Session, sucursal_id: int) -> Sucursal | None:
    return db.get(Sucursal, sucursal_id)


def get_producto(db: Session, producto_id: int) -> Producto | None:
    return db.get(Producto, producto_id)


def create(db: Session, *, sucursal_id: int, producto_id: int, cantidad: int, precio: float) -> tuple[Venta, VentaDetalle]:
    importe = cantidad * precio
    venta = Venta(sucursal_id=sucursal_id, fecha=datetime.now(timezone.utc), total=importe)
    db.add(venta)
    db.flush()
    detalle = VentaDetalle(venta_id=venta.id, producto_id=producto_id, cantidad=cantidad, importe=importe)
    db.add(detalle)
    db.commit()
    db.refresh(venta)
    db.refresh(detalle)
    return venta, detalle
