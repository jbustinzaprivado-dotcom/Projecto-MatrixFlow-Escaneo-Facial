"""Límite de peticiones en memoria de un proceso [Añadido, Fase A]. Solo protege
`/verificacion`, el único endpoint sin sesión de todo el backend — el resto no tiene límite
propio porque tampoco tiene autenticación todavía (Fase 6, si se decide construirla).
"""

import threading
import time
from collections import deque


class SlidingWindowLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str, limit: int, window: float = 60.0) -> bool:
        ahora = time.monotonic()
        with self._lock:
            hits = self._hits.setdefault(key, deque())
            while hits and hits[0] <= ahora - window:
                hits.popleft()
            if len(hits) >= limit:
                return False
            hits.append(ahora)
            return True


verificacion_limiter = SlidingWindowLimiter()
