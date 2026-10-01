from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.api.routes.acceso import audit, location, users
from app.api.routes.algebra import matrices, operations, vectors
from app.api.routes.biometria import verification
from app.api.routes.empresa import branches, companies, products
from app.api.routes.operacion import inventory, sales, targets
from app.api.routes.reportes import dashboard, reports
from app.core.config import get_settings
from app.core.errors import ApiException

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ApiException)
def handle_api_exception(_request: Request, exc: ApiException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


# Desde la Fase 6 [PDF §13]: sin auth.py de usuario/contraseña (D17) — la sesión (JWT) la
# emite `POST /verificacion` al coincidir (D70). RBAC por rol vía las dependencias de
# app/api/deps.py (CurrentUser, RequireEscritura, RequireAdmin) en cada router.
API_PREFIX = "/api/v1"
app.include_router(companies.router, prefix=API_PREFIX)
app.include_router(branches.router, prefix=API_PREFIX)
app.include_router(products.router, prefix=API_PREFIX)
app.include_router(sales.router, prefix=API_PREFIX)
app.include_router(inventory.router, prefix=API_PREFIX)
app.include_router(vectors.router, prefix=API_PREFIX)
app.include_router(matrices.router, prefix=API_PREFIX)
app.include_router(operations.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(verification.router, prefix=API_PREFIX)
app.include_router(audit.router, prefix=API_PREFIX)
app.include_router(location.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(targets.router, prefix=API_PREFIX)


@app.get("/api/health")
def health():
    return {"status": "ok"}
