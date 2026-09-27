from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Producto, Sucursal, Venta, VentaDetalle
from app.schemas.report_schema import ReporteOut, VentasPorProducto, VentasPorSucursal


def build_reporte(db: Session) -> ReporteOut:
    por_sucursal = db.execute(
        select(Sucursal.nombre, func.coalesce(func.sum(Venta.total), 0))
        .outerjoin(Venta, Venta.sucursal_id == Sucursal.id)
        .group_by(Sucursal.id)
        .order_by(Sucursal.id)
    ).all()
    por_producto = db.execute(
        select(Producto.nombre, func.coalesce(func.sum(VentaDetalle.cantidad), 0))
        .outerjoin(VentaDetalle, VentaDetalle.producto_id == Producto.id)
        .group_by(Producto.id)
        .order_by(Producto.id)
    ).all()
    return ReporteOut(
        ventas_por_sucursal=[VentasPorSucursal(sucursal=n, importe=float(i)) for n, i in por_sucursal],
        ventas_por_producto=[VentasPorProducto(producto=n, cantidad=int(c)) for n, c in por_producto],
    )
