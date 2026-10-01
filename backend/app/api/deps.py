from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.core.security import decodificar_token
from app.database.connection import get_db
from app.models import Usuario
from app.repositories.acceso import user_repository

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession, authorization: Annotated[str | None, Header()] = None
) -> Usuario:
    """[Añadido, Fase 6] Exige la sesión que abre `POST /verificacion` al coincidir (D70).
    Sin usuario/contraseña: la única forma de obtener un token es el login biométrico."""
    if not authorization or not authorization.startswith("Bearer "):
        raise ApiException(401, "Sesión requerida. Ingresa por DNI y verificación facial.")

    payload = decodificar_token(authorization.removeprefix("Bearer "))
    if payload is None:
        raise ApiException(401, "La sesión no es válida o expiró. Ingresa de nuevo.")

    usuario = user_repository.get(db, int(payload["sub"]))
    if usuario is None or not usuario.activo:
        raise ApiException(401, "La sesión no es válida o expiró. Ingresa de nuevo.")
    return usuario


CurrentUser = Annotated[Usuario, Depends(get_current_user)]


def require_administrador(usuario: CurrentUser) -> Usuario:
    """[Añadido, Fase 6] Solo administrador: alta de usuarios y registro de rostros (D71)."""
    if usuario.rol.nombre != "administrador":
        raise ApiException(403, "Esta acción requiere el rol administrador.")
    return usuario


def require_escritura(usuario: CurrentUser) -> Usuario:
    """[Añadido, Fase 6] Administrador o analista pueden crear/editar datos de negocio;
    consulta queda en solo lectura (D71)."""
    if usuario.rol.nombre not in ("administrador", "analista"):
        raise ApiException(403, "Tu rol (consulta) solo tiene acceso de lectura.")
    return usuario


RequireAdmin = Annotated[Usuario, Depends(require_administrador)]
RequireEscritura = Annotated[Usuario, Depends(require_escritura)]
