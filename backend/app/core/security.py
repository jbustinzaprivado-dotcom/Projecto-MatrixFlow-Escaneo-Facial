"""Sesión real emitida por la verificación facial [Añadido, Fase 6 — corrige D44]. El
login no es usuario/contraseña (D17): el propio `POST /verificacion` emite este JWT cuando
el rostro coincide con el DNI ingresado, según el rol del usuario encontrado (D6)."""

from datetime import timedelta

import jwt

from app.core.config import get_settings
from app.database.types import utcnow

ALGORITMO = "HS256"


def crear_token(usuario_id: int, rol: str) -> str:
    settings = get_settings()
    ahora = utcnow()
    payload = {
        "sub": str(usuario_id),
        "rol": rol,
        "iat": ahora,
        "exp": ahora + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITMO)


def decodificar_token(token: str) -> dict | None:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITMO])
    except jwt.PyJWTError:
        return None
