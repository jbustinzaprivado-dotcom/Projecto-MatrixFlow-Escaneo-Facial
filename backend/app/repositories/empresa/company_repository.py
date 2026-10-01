from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Empresa


def get_empresa(db: Session) -> Empresa | None:
    return db.scalar(select(Empresa).limit(1))
