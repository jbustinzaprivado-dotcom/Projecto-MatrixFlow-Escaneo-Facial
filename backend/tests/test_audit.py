"""Auditoría real (D73): agrega `audit_logs`, que cada verificación escribe."""

import numpy as np
import pytest

from app.services import verification_service
from app.services.face_engine import engine
from app.services.face_engine.engine import RostroRechazado

FOTO_CORRECTA = b"foto-correcta"
VECTOR_REGISTRADO = np.array([1.0, 0.0, 0.0], dtype=np.float32)


def _embedding_simulado(imagen_bytes: bytes) -> np.ndarray:
    if imagen_bytes == FOTO_CORRECTA:
        return VECTOR_REGISTRADO
    raise RostroRechazado("No se detectó un rostro.")


@pytest.fixture(autouse=True)
def _motor_facial_simulado(monkeypatch):
    monkeypatch.setattr(engine, "modelos_disponibles", lambda: True)
    monkeypatch.setattr(engine, "calcular_embedding", _embedding_simulado)


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_auditoria_muestra_sede_y_ranking_reales(client, db, usuarios, tokens):
    admin = usuarios["administrador"]
    verification_service.registrar_rostro(db, admin.id, FOTO_CORRECTA)

    # Dos logins correctos del administrador, uno fallido con un DNI inexistente.
    verification_service.verificar(db, admin.dni, FOTO_CORRECTA)
    verification_service.verificar(db, admin.dni, FOTO_CORRECTA)
    verification_service.verificar(db, "00000000", FOTO_CORRECTA)
    db.commit()

    respuesta = client.get("/api/v1/audit", headers=auth(tokens["administrador"]))
    assert respuesta.status_code == 200
    filas = respuesta.json()
    assert len(filas) == 3
    assert any(f["usuario"] == admin.nombre and f["resultado"] == "ok" and f["sede"] == "Sede prueba" for f in filas)
    assert any(f["usuario"] == "Desconocido" and f["resultado"] == "error" for f in filas)

    resumen = client.get("/api/v1/audit/resumen", headers=auth(tokens["administrador"])).json()
    assert resumen["total_7_dias"] == 3
    assert resumen["mas_activos"][0] == {"usuario": admin.nombre, "cantidad": 2}
