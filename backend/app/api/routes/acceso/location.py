from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession, RequireAdmin
from app.schemas.acceso.location_schema import UbicacionActivaOut, UbicacionIn
from app.services.acceso import location_service

router = APIRouter(prefix="/ubicacion", tags=["ubicacion"])


@router.post("", status_code=204)
def reportar_ubicacion(payload: UbicacionIn, db: DbSession, usuario: CurrentUser) -> None:
    """[Añadido, corrige D9] Cualquier rol autenticado reporta su propia posición; la
    identidad sale del JWT (CurrentUser), nunca de un id que mande el cliente."""
    location_service.reportar(
        db,
        usuario_id=usuario.id,
        latitud=payload.latitud,
        longitud=payload.longitud,
        precision_m=payload.precision_m,
    )


@router.get("/activas", response_model=list[UbicacionActivaOut])
def listar_ubicaciones_activas(db: DbSession, _usuario: RequireAdmin):
    """[Añadido, corrige D9] Solo administrador: mapa en vivo dentro de Auditoría (D133)."""
    return location_service.listar_activas(db)
