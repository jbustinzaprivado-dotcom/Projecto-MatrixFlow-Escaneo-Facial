from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Operacion, OperacionEntrada, OperacionResultado


def create(
    db: Session,
    *,
    tipo: str,
    estado: str,
    mensaje: str,
    entradas: list[dict],
    resultado: str | None = None,
) -> Operacion:
    """`entradas` es una lista de dicts como {"rol": "a", "tipo_entrada": "vector",
    "referencia_id": 1} o {"rol": "b", "tipo_entrada": "escalar", "valor_escalar": 2.5}.
    `resultado` solo se guarda en `operation_results` cuando el cálculo se hizo de verdad
    (Fase 4, [PDF §11]); si es `None` (pendiente o error) esa tabla no recibe fila."""
    operacion = Operacion(
        tipo=tipo,
        estado=estado,
        mensaje=mensaje,
        creado_en=datetime.now(timezone.utc),
    )
    db.add(operacion)
    db.flush()
    db.add_all(OperacionEntrada(operation_id=operacion.id, **entrada) for entrada in entradas)
    if resultado is not None:
        db.add(OperacionResultado(operation_id=operacion.id, resultado=resultado))
    db.commit()
    db.refresh(operacion)
    return get(db, operacion.id)  # type: ignore[return-value]


def get(db: Session, operation_id: int) -> Operacion | None:
    return db.scalar(
        select(Operacion)
        .options(selectinload(Operacion.entradas), selectinload(Operacion.resultado))
        .where(Operacion.id == operation_id)
    )


def list_all(db: Session) -> list[Operacion]:
    return list(
        db.scalars(
            select(Operacion)
            .options(selectinload(Operacion.entradas), selectinload(Operacion.resultado))
            .order_by(Operacion.id)
        )
    )
