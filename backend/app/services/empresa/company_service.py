from sqlalchemy.orm import Session

from app.models import Empresa
from app.repositories.empresa import company_repository


def get_empresa(db: Session) -> Empresa | None:
    return company_repository.get_empresa(db)
