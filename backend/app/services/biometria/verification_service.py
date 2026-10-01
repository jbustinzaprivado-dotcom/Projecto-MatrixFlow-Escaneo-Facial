"""Registro y verificación de rostro [Añadido, Fase A]. Identificación 1:1 (D6): el DNI
busca a un único usuario y su rostro solo se compara contra los propios vectores guardados
de esa persona, nunca contra toda la base. Sin candidato cuando no coincide (D80): jamás se
dice quién era, ni siquiera al equipo que llama al endpoint.

Desde la Fase A2, **cada** intento de verificación queda registrado en
`verificacion_intentos` — coincida o no, con el DNI ingresado (decisión del equipo).

Desde la Fase 6, al coincidir se emite además un JWT real (D70, corrige D44): esta
verificación deja de ser solo identificación y pasa a ser el mecanismo de acceso al resto
del sistema, según el rol del usuario encontrado (D6). Cada intento también escribe una fila
en `audit_logs` [PDF §10] (D73): es la tabla del documento que existía desde la Fase 3 sin
usarse (D35), y ahora es la fuente real de la Auditoría extendida (D5).
"""

from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.core.security import crear_token
from app.models import Usuario
from app.repositories.acceso import audit_repository, user_repository
from app.repositories.biometria import face_repository, verification_repository
from app.schemas.acceso.user_schema import RostroOut, VerificacionOut, VerificacionUsuario
from app.services.biometria.face_engine import engine
from app.services.biometria.face_engine.engine import RostroRechazado

ACCION_LOGIN = "Inicio de sesión"
RECURSO_LOGIN = "Login biométrico (DNI + rostro)"


def _registrar_intento(
    db: Session,
    *,
    dni: str,
    usuario: Usuario | None,
    coincide: bool,
    similitud: float | None,
    detalle: str | None = None,
) -> None:
    """Escribe el mismo intento en dos tablas con audiencias distintas: `verificacion_intentos`
    (Fase A2, técnico, solo administrador, incluye similitud) y `audit_logs` (Fase 6, D73,
    lectura para cualquier rol, es la Auditoría que ve el equipo)."""
    verification_repository.add(
        db, dni=dni, usuario_id=usuario.id if usuario else None, coincide=coincide, similitud=similitud
    )
    audit_repository.add(
        db,
        usuario_id=usuario.id if usuario else None,
        accion=ACCION_LOGIN,
        recurso=RECURSO_LOGIN,
        resultado="ok" if coincide else "error",
        detalle=detalle,
        sucursal_id=usuario.sucursal_id if usuario else None,
    )


def registrar_rostro(db: Session, usuario_id: int, imagen_bytes: bytes) -> RostroOut:
    usuario = user_repository.get(db, usuario_id)
    if usuario is None:
        raise ApiException(404, "El usuario no existe.")
    if not engine.modelos_disponibles():
        raise ApiException(503, "El motor facial no está disponible en este entorno.")

    try:
        vector = engine.calcular_embedding(imagen_bytes)
    except RostroRechazado as error:
        raise ApiException(422, str(error)) from None

    face_repository.add(db, usuario_id=usuario.id, embedding=engine.a_bytes(vector), modelo=engine.MODELO_NOMBRE)
    total = len(face_repository.list_by_usuario(db, usuario.id, engine.MODELO_NOMBRE))
    return RostroOut(usuario_id=usuario.id, imagenes_guardadas=total)


def verificar(db: Session, dni: str, imagen_bytes: bytes) -> VerificacionOut:
    if not engine.modelos_disponibles():
        raise ApiException(503, "El motor facial no está disponible en este entorno.")

    usuario = user_repository.get_by_dni(db, dni)
    if usuario is None or not usuario.activo:
        # Mismo resultado que "no coincide": no se revela si el DNI existe (D80).
        _registrar_intento(
            db, dni=dni, usuario=None, coincide=False, similitud=None, detalle="DNI no registrado"
        )
        return VerificacionOut(coincide=False, similitud=0.0)

    guardados = face_repository.list_by_usuario(db, usuario.id, engine.MODELO_NOMBRE)
    if not guardados:
        _registrar_intento(
            db,
            dni=dni,
            usuario=usuario,
            coincide=False,
            similitud=None,
            detalle="Usuario sin rostro registrado",
        )
        raise ApiException(409, "Este usuario aún no tiene un rostro registrado.")

    try:
        vector = engine.calcular_embedding(imagen_bytes)
    except RostroRechazado as error:
        _registrar_intento(
            db,
            dni=dni,
            usuario=usuario,
            coincide=False,
            similitud=None,
            detalle="Imagen sin rostro detectable",
        )
        raise ApiException(422, str(error)) from None

    mejor = max(
        engine.similitud_coseno(vector, engine.desde_bytes(rostro.embedding)) for rostro in guardados
    )
    coincide = mejor >= engine.UMBRAL_SIMILITUD
    _registrar_intento(
        db,
        dni=dni,
        usuario=usuario,
        coincide=coincide,
        similitud=mejor,
        detalle=None if coincide else "Rostro no coincide con el registrado",
    )

    if not coincide:
        return VerificacionOut(coincide=False, similitud=mejor)

    return VerificacionOut(
        coincide=True,
        similitud=mejor,
        usuario=VerificacionUsuario(
            nombre=usuario.nombre,
            dni=usuario.dni,
            rol=usuario.rol.nombre,
            sede=usuario.sucursal.nombre if usuario.sucursal else "—",
            activo=usuario.activo,
            creado_en=usuario.creado_en,
        ),
        token=crear_token(usuario.id, usuario.rol.nombre),
    )


def list_intentos(db: Session):
    return verification_repository.list_all(db)
