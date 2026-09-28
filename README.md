# MatrixFlow

Sistema web empresarial de análisis de ventas, inventario e indicadores mediante álgebra
lineal — desarrollado siguiendo `MatrixFlow_Enterprise_Plan_Desarrollo.pdf` (Plan Maestro
de Desarrollo). El registro completo de decisiones, fase por fase, está en
[`docs/PROCESO.md`](docs/PROCESO.md).

**Stack:** React + TypeScript + Vite · Python + FastAPI · PostgreSQL · NumPy.

## Estructura

```
matrixflow-enterprise/
├── frontend/    React + TypeScript + Vite
├── backend/     FastAPI + SQLAlchemy + NumPy + OpenCV (login biométrico)
├── docs/        docs/PROCESO.md — decisiones documentadas por fase
├── docker-compose.yml
└── .env.example
```

## Desarrollo local (sin Docker)

Requisitos: Python 3.11+, Node 20+, PostgreSQL 16.

```bash
# Base de datos
createdb matrixflow

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # ajusta DATABASE_URL si hace falta
alembic upgrade head
python -m app.scripts.seed   # datos de ejemplo (opcional)
uvicorn app.main:app --reload

# Frontend (otra terminal)
cd frontend
npm install
npm run dev
```

Frontend en `http://localhost:5173`, backend en `http://localhost:8000` (`/docs` para Swagger).

### Motor facial (login por DNI + rostro)

El login (`/ingresar`) necesita dos modelos de OpenCV que **no están en el repositorio**
(pesan ~39 MB, ignorados por git a propósito). Para desarrollo local sin Docker,
descárgalos a `backend/models/`:

- `face_detection_yunet_2023mar.onnx`
- `face_recognition_sface_2021dec.onnx`

Ambos vienen de [opencv/opencv_zoo](https://github.com/opencv/opencv_zoo) (usa
`media.githubusercontent.com`, no `raw.githubusercontent.com` — ese repo los versiona con
Git LFS y `raw` solo da el puntero de texto). Sin ellos, `POST /verificacion` y el registro
de rostro responden `503`; el resto del sistema funciona igual.

## Con Docker

```bash
cp .env.example .env
docker compose up --build
```

El `Dockerfile` del backend descarga los pesos ONNX automáticamente durante el build si no
los encuentra ya en `backend/models/` — no hace falta el paso manual de arriba.

## Despliegue público (en preparación)

El proyecto está pensado para desplegarse con **Vercel** (frontend), **Render** (backend) y
**Supabase** (PostgreSQL). Ya existen `render.yaml` (Blueprint del backend) y
`frontend/vercel.json` (necesario para que las rutas de React Router funcionen en Vercel),
pero las cuentas y el repositorio de GitHub aún no se han creado — cuando llegue ese
momento, pide la guía paso a paso.

Levanta PostgreSQL, el backend (con migraciones automáticas) y el frontend (servido por
nginx) en `http://localhost:5173`.

## Pruebas

```bash
cd backend
createdb matrixflow_test   # una vez
pytest tests/ -v
```

Corren contra una base de datos Postgres real y separada (`matrixflow_test`), con
aislamiento transaccional por prueba — no tocan `matrixflow` (desarrollo).

## Cuentas de ejemplo (tras `python -m app.scripts.seed`)

No hay usuario/contraseña (D17): se entra por DNI + verificación facial. Los DNIs
sembrados no tienen rostro registrado por defecto — usa `Usuarios` (como administrador)
para registrar uno real, o revisa `docs/PROCESO.md` (Fase A) para el detalle del flujo.

| Rol | DNI |
|---|---|
| Administrador | 71234567 |
| Analista | 72345678 |
| Consulta | 73456789 |
