from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireEscritura
from app.schemas.operacion.inventory_schema import InventarioOut, MovimientoCreate, MovimientoOut
from app.services.operacion import inventory_service

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=list[InventarioOut])
def list_inventory(db: DbSession, _usuario: CurrentUser):
    return inventory_service.list_inventario(db)


@router.post("/movimientos", response_model=MovimientoOut, status_code=201)
def create_movimiento(data: MovimientoCreate, db: DbSession, _usuario: RequireEscritura):
    """[RF-06, Añadido en el repaso de fidelidad §16-21] Administrador o analista (§13)."""
    return inventory_service.registrar_movimiento(db, data)
