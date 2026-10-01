from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Usuario


def list_all(db: Session) -> list[Usuario]:
    return list(
        db.scalars(
            select(Usuario)
            .options(selectinload(Usuario.rol), selectinload(Usuario.rostros))
            .order_by(Usuario.id)
        )
    )


def get(db: Session, usuario_id: int) -> Usuario | None:
    return db.scalar(
        select(Usuario)
        .options(selectinload(Usuario.rol), selectinload(Usuario.sucursal), selectinload(Usuario.rostros))
        .where(Usuario.id == usuario_id)
    )


def get_by_dni(db: Session, dni: str) -> Usuario | None:
    return db.scalar(
        select(Usuario)
        .options(selectinload(Usuario.rol), selectinload(Usuario.rostros))
        .where(Usuario.dni == dni)
    )


def get_by_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email))


def create(db: Session, *, nombre: str, email: str, dni: str, rol_id: int, sucursal_id: int) -> Usuario:
    usuario = Usuario(nombre=nombre, email=email, dni=dni, rol_id=rol_id, sucursal_id=sucursal_id)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return get(db, usuario.id)  # type: ignore[return-value]
