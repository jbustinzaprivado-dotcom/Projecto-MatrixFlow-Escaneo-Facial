from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.acceso.audit_schema import AuditoriaEntradaOut, AuditoriaResumenOut
from app.services.acceso import audit_service

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditoriaEntradaOut])
def list_audit(db: DbSession, _usuario: CurrentUser):
    """[Añadido D5, D9] Cualquier rol autenticado puede consultarla — es de solo lectura."""
    return audit_service.listar(db)


@router.get("/resumen", response_model=AuditoriaResumenOut)
def audit_resumen(db: DbSession, _usuario: CurrentUser):
    return audit_service.resumen(db)
