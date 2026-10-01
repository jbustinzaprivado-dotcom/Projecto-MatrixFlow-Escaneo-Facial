from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.repositories.operacion import sale_repository
from app.schemas.operacion.sale_schema import VentaCreate, VentaOut


def list_ventas(db: Session) -> list[VentaOut]:
    return [
        VentaOut(
            id=venta.id,
            sucursal_id=venta.sucursal_id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            importe=float(detalle.importe),
            fecha=venta.fecha,
        )
        for venta, detalle in sale_repository.list_all(db)
    ]


def create_venta(db: Session, data: VentaCreate) -> VentaOut:
    sucursal = sale_repository.get_sucursal(db, data.sucursal_id)
    if sucursal is None:
        raise ApiException(404, "La sucursal no existe.")
    producto = sale_repository.get_producto(db, data.producto_id)
    if producto is None:
        raise ApiException(404, "El producto no existe.")

    venta, detalle = sale_repository.create(
        db,
        sucursal_id=sucursal.id,
        producto_id=producto.id,
        cantidad=data.cantidad,
        precio=float(producto.precio),
    )
    return VentaOut(
        id=venta.id,
        sucursal_id=venta.sucursal_id,
        producto_id=detalle.producto_id,
        cantidad=detalle.cantidad,
        importe=float(detalle.importe),
        fecha=venta.fecha,
    )
