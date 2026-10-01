from typing import Annotated

from fastapi import APIRouter, File, Form, Request, UploadFile

from app.api.deps import DbSession, RequireAdmin
from app.core.errors import ApiException
from app.core.rate_limit import verificacion_limiter
from app.schemas.acceso.user_schema import VerificacionIntentoOut, VerificacionOut
from app.services.biometria import verification_service

router = APIRouter(prefix="/verificacion", tags=["verificacion"])

MAX_IMAGE_BYTES = 5 * 1024 * 1024
LIMITE_POR_MINUTO = 10  # endpoint sin sesión: mismo orden de magnitud que un límite de login


@router.post("", response_model=VerificacionOut)
async def verificar(
    request: Request, db: DbSession, dni: Annotated[str, Form()], imagen: Annotated[UploadFile, File()]
):
    """Sin sesión: es el propio mecanismo para obtenerla (D70). Identifica y devuelve los
    datos de la persona si coincide, con el JWT de acceso, o `coincide: false` sin nombrar a
    nadie si no (D6, D80)."""
    ip = request.client.host if request.client else "desconocida"
    if not verificacion_limiter.allow(ip, LIMITE_POR_MINUTO):
        raise ApiException(429, "Demasiados intentos. Espera un minuto y vuelve a intentarlo.")

    if not dni.isdigit() or len(dni) != 8:
        raise ApiException(422, "El DNI debe tener exactamente 8 dígitos.")
    data = await imagen.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise ApiException(413, "La imagen pesa más de 5 MB.")
    return verification_service.verificar(db, dni, data)


@router.get("", response_model=list[VerificacionIntentoOut])
def historial(db: DbSession, _usuario: RequireAdmin):
    """[Añadido, Fase A2] Cada intento queda aquí, coincida o no. Solo administrador desde
    la Fase 6: incluye DNIs que nunca llegaron a coincidir."""
    return verification_service.list_intentos(db)
