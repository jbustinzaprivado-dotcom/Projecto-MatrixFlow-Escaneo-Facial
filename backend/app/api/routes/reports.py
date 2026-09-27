from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.report_schema import ReporteOut
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=ReporteOut)
def get_reports(db: DbSession, _usuario: CurrentUser):
    return report_service.build_reporte(db)
