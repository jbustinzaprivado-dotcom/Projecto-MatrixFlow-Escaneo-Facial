"""Bootstrap [Añadido]: registra un rostro real para un usuario ya sembrado, sin pasar por
`POST /users/{id}/rostro` (que exige RequireAdmin, D71) — un candado que ningún administrador
puede abrir todavía en una base de datos recién desplegada, sin un solo rostro registrado.
Mismo mecanismo que D109 ya usó para sembrar rostros de demostración en desarrollo; aquí se
expone como script de un solo uso para poder hacerlo también contra producción.

Uso: venv/bin/python -m app.scripts.registrar_rostro <DNI> <ruta_a_la_foto.jpg>
"""

import sys

from app.database.connection import SessionLocal
from app.repositories import face_repository, user_repository
from app.services.face_engine import engine
from app.services.face_engine.engine import RostroRechazado


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python -m app.scripts.registrar_rostro <DNI> <ruta_a_la_foto.jpg>")
        raise SystemExit(1)

    dni, ruta = sys.argv[1], sys.argv[2]

    if not engine.modelos_disponibles():
        print("Los modelos ONNX no están en backend/models/ — revisa el README (sección 'Motor facial').")
        raise SystemExit(1)

    with open(ruta, "rb") as archivo:
        imagen_bytes = archivo.read()

    db = SessionLocal()
    try:
        usuario = user_repository.get_by_dni(db, dni)
        if usuario is None:
            print(f"No existe ningún usuario con DNI {dni}. Corre primero: python -m app.scripts.seed")
            raise SystemExit(1)

        try:
            vector = engine.calcular_embedding(imagen_bytes)
        except RostroRechazado as error:
            print(f"La foto fue rechazada: {error}")
            raise SystemExit(1)

        face_repository.add(
            db, usuario_id=usuario.id, embedding=engine.a_bytes(vector), modelo=engine.MODELO_NOMBRE
        )
        print(f"Rostro registrado para {usuario.nombre} (DNI {dni}, rol {usuario.rol.nombre}).")
    finally:
        db.close()


if __name__ == "__main__":
    main()