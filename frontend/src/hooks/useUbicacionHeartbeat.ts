import { useEffect } from 'react'
import { reportarUbicacion } from '../services/api'

const INTERVALO_MS = 60_000

/** Heartbeat de ubicación en vivo [Añadido, corrige D9]: reporta la posición del
 * dispositivo cada ~60s mientras haya una sesión activa. Se monta una sola vez en
 * `Layout.tsx`, que solo existe dentro de `<RutaProtegida>` (App.tsx) — no hace falta
 * engancharse a `AuthContext` ni a eventos de login/logout por separado: montar/desmontar
 * Layout ya es, en la práctica, "sesión abierta"/"sesión cerrada".
 *
 * Si el navegador no soporta geolocalización, o la persona niega el permiso, falla en
 * silencio: la app completa debe seguir funcionando igual sin esto. */
export function useUbicacionHeartbeat() {
  useEffect(() => {
    if (!('geolocation' in navigator)) return

    let cancelado = false

    function reportar() {
      navigator.geolocation.getCurrentPosition(
        (posicion) => {
          if (cancelado) return
          reportarUbicacion({
            latitud: posicion.coords.latitude,
            longitud: posicion.coords.longitude,
            precisionM: posicion.coords.accuracy,
          }).catch(() => {
            // Latido perdido: no pasa nada, el siguiente intento es en 60s (D130).
          })
        },
        () => {
          // Permiso denegado / sin señal GPS / timeout: silencioso a propósito.
        },
        { enableHighAccuracy: false, maximumAge: INTERVALO_MS, timeout: 10_000 },
      )
    }

    reportar() // primer latido inmediato: no hacer esperar 60s para aparecer en el mapa
    const id = setInterval(reportar, INTERVALO_MS)
    return () => {
      cancelado = true
      clearInterval(id)
    }
  }, [])
}
