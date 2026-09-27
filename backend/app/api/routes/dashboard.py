from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.dashboard_schema import DashboardResumenOut
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResumenOut)
def get_dashboard(db: DbSession, _usuario: CurrentUser):
    return dashboard_service.build_resumen(db)
