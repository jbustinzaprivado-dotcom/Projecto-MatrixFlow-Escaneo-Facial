class DimensionError(ValueError):
    """Dimensiones incompatibles [PDF: criterio CA-06]. La capa de servicio la atrapa y la
    convierte en `estado: "error"` del historial, nunca en un error HTTP."""
