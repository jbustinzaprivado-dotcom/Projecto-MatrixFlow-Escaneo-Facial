from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.models import Sucursal
from app.repositories import branch_repository, company_repository
from app.schemas.branch_schema import SucursalCreate


def list_sucursales(db: Session) -> list[Sucursal]:
    return branch_repository.list_all(db)


def create_sucursal(db: Session, data: SucursalCreate) -> Sucursal:
    empresa = company_repository.get_empresa(db)
    if empresa is None:
        raise ApiException(500, "No hay una empresa registrada todavía.")
    return branch_repository.create(
        db,
        company_id=empresa.id,
        nombre=data.nombre,
        departamento=data.departamento,
        distrito=data.distrito,
        direccion=data.direccion,
    )
