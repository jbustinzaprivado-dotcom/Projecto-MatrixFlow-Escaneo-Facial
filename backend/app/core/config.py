from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración general de la app."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "MatrixFlow API"
    cors_origins: list[str] = ["http://localhost:5173"]
    database_url: str = "postgresql+psycopg2://matrixflow:matrixflow_dev@localhost:5432/matrixflow"

    # Fase 6 — Seguridad [PDF §13]. Clave por defecto solo para desarrollo local; en un
    # despliegue real se sobreescribe con la variable de entorno SECRET_KEY.
    secret_key: str = "matrixflow-dev-secret-cambiar-en-produccion"
    jwt_expire_minutes: int = 480  # 8 horas, un turno laboral


@lru_cache
def get_settings() -> Settings:
    return Settings()
