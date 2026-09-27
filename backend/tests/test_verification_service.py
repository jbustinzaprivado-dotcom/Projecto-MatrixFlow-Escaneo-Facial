"""Verificación facial (D6, D70, D80). El pipeline real de OpenCV (YuNet+SFace) ya se
verificó a mano con fotos reales en la Fase A (D45) y la Fase 6 (D78) — aquí se simula
`calcular_embedding`/`modelos_disponibles` para poner a prueba la lógica de negocio
(privacidad, emisión de JWT, registro en las dos tablas de historial) sin depender de los
pesos ONNX ni de fotos reales en el entorno de pruebas."""

import numpy as np
import pytest

from app.core.errors import ApiException
from app.core.security import decodificar_token
from app.repositories import audit_repository, verification_repository
from app.services import verification_service
from app.services.face_engine import engine
from app.services.face_engine.engine import RostroRechazado

FOTO_CORRECTA = b"foto-correcta"
FOTO_OTRA_PERSONA = b"foto-otra-persona"
FOTO_SIN_ROSTRO = b"foto-sin-rostro"

VECTOR_REGISTRADO = np.array([1.0, 0.0, 0.0], dtype=np.float32)
VECTOR_OTRA_PERSONA = np.array([0.0, 1.0, 0.0], dtype=np.float32)


def _embedding_simulado(imagen_bytes: bytes) -> np.ndarray:
    if imagen_bytes == FOTO_CORRECTA:
        return VECTOR_REGISTRADO
    if imagen_bytes == FOTO_OTRA_PERSONA:
        return VECTOR_OTRA_PERSONA
    raise RostroRechazado("No se detectó un rostro.")


@pytest.fixture(autouse=True)
def _motor_facial_simulado(monkeypatch):
    monkeypatch.setattr(engine, "modelos_disponibles", lambda: True)
    monkeypatch.setattr(engine, "calcular_embedding", _embedding_simulado)


def test_dni_inexistente_no_revela_nada(db):
    resultado = verification_service.verificar(db, "00000000", FOTO_CORRECTA)
    assert resultado.coincide is False
    assert resultado.usuario is None
    assert resultado.token is None
    assert resultado.similitud == 0.0


def test_dni_inexistente_queda_en_ambos_historiales(db):
    verification_service.verificar(db, "00000000", FOTO_CORRECTA)
    assert len(verification_repository.list_all(db)) == 1
    fila_auditoria = audit_repository.list_all(db)[0]
    assert fila_auditoria.resultado == "error"
    assert fila_auditoria.usuario is None


def test_usuario_sin_rostro_registrado_da_409(db, usuarios):
    usuario = usuarios["consulta"]
    with pytest.raises(ApiException) as exc_info:
        verification_service.verificar(db, usuario.dni, FOTO_CORRECTA)
    assert exc_info.value.status_code == 409


def test_imagen_sin_rostro_da_422(db, usuarios):
    usuario = usuarios["analista"]
    verification_service.registrar_rostro(db, usuario.id, FOTO_CORRECTA)
    with pytest.raises(ApiException) as exc_info:
        verification_service.verificar(db, usuario.dni, FOTO_SIN_ROSTRO)
    assert exc_info.value.status_code == 422


def test_rostro_correcto_coincide_y_emite_token(db, usuarios):
    usuario = usuarios["administrador"]
    verification_service.registrar_rostro(db, usuario.id, FOTO_CORRECTA)

    resultado = verification_service.verificar(db, usuario.dni, FOTO_CORRECTA)

    assert resultado.coincide is True
    assert resultado.usuario.nombre == usuario.nombre
    assert resultado.token is not None
    payload = decodificar_token(resultado.token)
    assert payload["sub"] == str(usuario.id)
    assert payload["rol"] == "administrador"


def test_rostro_de_otra_persona_no_revela_a_quien_se_parecia(db, usuarios):
    """D80: un DNI real con un rostro que no coincide da la misma forma de respuesta que un
    DNI inexistente — nunca se nombra a la persona buscada."""
    usuario = usuarios["analista"]
    verification_service.registrar_rostro(db, usuario.id, FOTO_CORRECTA)

    resultado = verification_service.verificar(db, usuario.dni, FOTO_OTRA_PERSONA)

    assert resultado.coincide is False
    assert resultado.usuario is None
    assert resultado.token is None


def test_no_coincidencia_igual_queda_registrada_con_el_dni(db, usuarios):
    """El intento sí deja rastro con el DNI ingresado (decisión del equipo, D58) aunque no
    se revele identidad en la respuesta al llamador."""
    usuario = usuarios["analista"]
    verification_service.registrar_rostro(db, usuario.id, FOTO_CORRECTA)
    verification_service.verificar(db, usuario.dni, FOTO_OTRA_PERSONA)

    intento = verification_repository.list_all(db)[0]
    assert intento.dni == usuario.dni
    assert intento.usuario_id == usuario.id
    assert intento.coincide is False
