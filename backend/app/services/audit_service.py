"""Auditoría extendida [Añadido D5, D9]. Desde la Fase 6 (D73) se lee de `audit_logs`
[PDF §10], que la Fase 3 dejó creada sin usar (D35) y que ahora escribe cada intento de
verificación (D70), coincida o no."""

from collections import Counter
from datetime import timedelta

from sqlalchemy.orm import Session

from app.database.types import utcnow
from app.models import Auditoria
from app.repositories import audit_repository

VENTANA_DIAS = 7


def _nombre_usuario(entrada: Auditoria) -> str:
    if entrada.usuario is not None:
        return entrada.usuario.nombre
    return "Desconocido"


def _sede(entrada: Auditoria) -> str:
    if entrada.usuario is not None and entrada.usuario.sucursal is not None:
        return entrada.usuario.sucursal.nombre
    return "—"


def listar(db: Session) -> list[dict]:
    return [
        {
            "id": entrada.id,
            "usuario": _nombre_usuario(entrada),
            "accion": entrada.accion,
            "recurso": entrada.recurso,
            "resultado": entrada.resultado,
            "fecha": entrada.creado_en,
            "sede": _sede(entrada),
        }
        for entrada in audit_repository.list_all(db)
    ]


def resumen(db: Session) -> dict:
    todas = audit_repository.list_all(db)
    corte = utcnow() - timedelta(days=VENTANA_DIAS)
    recientes = [entrada for entrada in todas if entrada.creado_en >= corte]

    por_dia = Counter(entrada.creado_en.date().isoformat() for entrada in recientes)
    por_usuario = Counter(
        entrada.usuario.nombre for entrada in recientes if entrada.resultado == "ok" and entrada.usuario
    )

    return {
        "actividad_por_dia": [
            {"dia": dia, "cantidad": cantidad} for dia, cantidad in sorted(por_dia.items())
        ],
        "mas_activos": [
            {"usuario": usuario, "cantidad": cantidad} for usuario, cantidad in por_usuario.most_common()
        ],
        "total_7_dias": len(recientes),
    }
