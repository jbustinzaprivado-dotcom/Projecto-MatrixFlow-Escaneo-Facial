from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireAdmin
from app.schemas.empresa.branch_schema import SucursalCreate, SucursalOut
from app.services.empresa import branch_service

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("", response_model=list[SucursalOut])
def list_branches(db: DbSession, _usuario: CurrentUser):
    return branch_service.list_sucursales(db)


@router.post("", response_model=SucursalOut, status_code=201)
def create_branch(data: SucursalCreate, db: DbSession, _usuario: RequireAdmin):
    """Solo administrador [corrige D71, repaso §16-21]: §13 no le da a analista acceso de
    escritura sobre "empresa" (sucursales son un sub-recurso de empresa en la navegación,
    §8.2), y CA-02 dice literalmente "el administrador puede registrar sucursales"."""
    return branch_service.create_sucursal(db, data)
