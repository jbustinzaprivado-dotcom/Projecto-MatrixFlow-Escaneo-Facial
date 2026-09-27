"""Manejo de errores de la Fase 2. Sin un sobre de respuesta propio (tipo `{success, resultado}`):
el documento no pide ningún formato de error en particular, así que se usa el que trae FastAPI
por defecto (`{"detail": "..."}`), sin inventar una convención que nadie pidió.
"""


class ValidationMessage(ValueError):
    """Se levanta dentro de un `field_validator` de Pydantic; se convierte solo en un 422."""


class ApiException(Exception):
    """Error de negocio con su código HTTP (404, 409, etc.), atrapado en `main.py`."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(message)
