from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireEscritura
from app.schemas.algebra.operation_schema import OperacionCreate, OperacionOut
from app.services.algebra import operation_service

router = APIRouter(prefix="/operations", tags=["operations"])


@router.post("", response_model=OperacionOut, status_code=201)
def create_operation(data: OperacionCreate, db: DbSession, _usuario: RequireEscritura):
    """Valida las entradas y las dimensiones, y guarda el intento en el historial.
    El resultado numérico llega en la Fase 4 [PDF §11]: hasta entonces queda "pendiente"."""
    return operation_service.create_operacion(db, data)


@router.get("", response_model=list[OperacionOut])
def list_operations(db: DbSession, _usuario: CurrentUser):
    return operation_service.list_historial(db)
