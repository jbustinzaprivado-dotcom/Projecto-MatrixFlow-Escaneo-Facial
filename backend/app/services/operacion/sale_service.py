from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.repositories.operacion import inventory_repository, sale_repository
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

    # [Añadido, corrige hallazgo del análisis de código] Una venta es, en el fondo, una salida
    # de inventario: sin este ajuste, Ventas e Inventario quedaban como dos registros
    # independientes que podían contradecirse entre sí (se podía "vender" stock que ya no
    # existía). Mismo criterio de "no existencias negativas" que ya aplica
    # inventory_service.registrar_movimiento, y las mismas funciones de repositorio.
    inventario = inventory_repository.get_or_create(db, sucursal.id, producto.id)
    if data.cantidad > inventario.existencias:
        raise ApiException(422, f"No hay suficientes existencias: quedan {inventario.existencias}.")

    venta, detalle = sale_repository.create(
        db,
        sucursal_id=sucursal.id,
        producto_id=producto.id,
        cantidad=data.cantidad,
        precio=float(producto.precio),
    )
    inventory_repository.add_movimiento(
        db, inventario_id=inventario.id, tipo="salida", cantidad=data.cantidad
    )
    inventory_repository.ajustar_existencias(db, inventario, -data.cantidad)

    return VentaOut(
        id=venta.id,
        sucursal_id=venta.sucursal_id,
        producto_id=detalle.producto_id,
        cantidad=detalle.cantidad,
        importe=float(detalle.importe),
        fecha=venta.fecha,
    )
