from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.models import Inventario, MovimientoInventario
from app.repositories.operacion import inventory_repository
from app.schemas.operacion.inventory_schema import MovimientoCreate


def list_inventario(db: Session) -> list[Inventario]:
    return inventory_repository.list_all(db)


def registrar_movimiento(db: Session, data: MovimientoCreate) -> MovimientoInventario:
    """[RF-06, Añadido en el repaso de fidelidad §16-21] Una salida no puede dejar existencias
    negativas — la misma validación de sentido común que ya aplica CA-06 a las dimensiones."""
    inventario = inventory_repository.get_or_create(db, data.sucursal_id, data.producto_id)
    if data.tipo == "salida" and data.cantidad > inventario.existencias:
        raise ApiException(
            422, f"No hay suficientes existencias: quedan {inventario.existencias}."
        )

    movimiento = inventory_repository.add_movimiento(
        db, inventario_id=inventario.id, tipo=data.tipo, cantidad=data.cantidad
    )
    delta = data.cantidad if data.tipo == "entrada" else -data.cantidad
    inventory_repository.ajustar_existencias(db, inventario, delta)
    return movimiento
