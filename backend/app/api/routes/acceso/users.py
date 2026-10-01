from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.api.deps import CurrentUser, DbSession, RequireAdmin
from app.core.errors import ApiException
from app.schemas.acceso.user_schema import CarnetOut, RostroOut, UsuarioCreate, UsuarioOut
from app.services.acceso import user_service
from app.services.biometria import verification_service

router = APIRouter(prefix="/users", tags=["users"])

MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB, mismo límite que Aurora ya probó razonable


async def _leer_imagen(imagen: UploadFile) -> bytes:
    data = await imagen.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise ApiException(413, "La imagen pesa más de 5 MB.")
    return data


@router.get("", response_model=list[UsuarioOut])
def list_users(db: DbSession, _usuario: CurrentUser):
    return user_service.list_usuarios(db)


@router.post("", response_model=UsuarioOut, status_code=201)
def create_user(data: UsuarioCreate, db: DbSession, _usuario: RequireAdmin):
    """Solo administrador [Añadido, Fase 6, D71]: dar de alta usuarios es una acción de
    gestión de cuentas, no de operación diaria del negocio."""
    return user_service.create_usuario(db, data)


@router.post("/{usuario_id}/rostro", response_model=RostroOut, status_code=201)
async def add_face(
    usuario_id: int, db: DbSession, imagen: Annotated[UploadFile, File()], _usuario: RequireAdmin
):
    """Registra un rostro para este usuario [Añadido, Fase A]. Una foto por llamada; se
    puede llamar varias veces para guardar más de una (no reemplaza las anteriores).
    Solo administrador (Fase 6, D71): mismo criterio que crear el usuario."""
    data = await _leer_imagen(imagen)
    return verification_service.registrar_rostro(db, usuario_id, data)


@router.get("/{usuario_id}/carnet", response_model=CarnetOut)
def get_carnet(usuario_id: int, db: DbSession, _usuario: CurrentUser):
    return user_service.get_carnet(db, usuario_id)
