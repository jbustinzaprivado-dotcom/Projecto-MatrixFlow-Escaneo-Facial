import { useEffect, useRef, useState } from 'react'

export type NivelIluminacion = 'oscuro' | 'buena' | 'brillante' | 'sin-señal'

// Límites provisionales [Añadido D5], sin calibrar con cámaras reales todavía (misma
// advertencia que el proyecto de referencia hizo con sus propios límites de calidad).
const UMBRAL_BAJO = 60
const UMBRAL_ALTO = 200
const INTERVALO_MS = 500
const MUESTREO_PX = 32

/** Brillo promedio del cuadro de video actual, muestreado cada 500 ms en un canvas oculto.
 * Es solo una guía visual para la persona que se registra o verifica: la decisión real de
 * calidad de imagen la toma el backend cuando exista (Fase 4). */
export function useBrillo(videoRef: React.RefObject<HTMLVideoElement | null>, activo: boolean) {
  const [brillo, setBrillo] = useState<number | null>(null)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  useEffect(() => {
    if (!activo) return
    if (!canvasRef.current) canvasRef.current = document.createElement('canvas')
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d', { willReadFrequently: true })
    let cancelado = false
    let temporizador: ReturnType<typeof setTimeout>

    function medir() {
      const video = videoRef.current
      if (video && ctx && video.videoWidth > 0) {
        canvas.width = MUESTREO_PX
        canvas.height = MUESTREO_PX
        ctx.drawImage(video, 0, 0, MUESTREO_PX, MUESTREO_PX)
        const { data } = ctx.getImageData(0, 0, MUESTREO_PX, MUESTREO_PX)
        let suma = 0
        for (let i = 0; i < data.length; i += 4) {
          suma += 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2]
        }
        setBrillo(suma / (data.length / 4))
      }
      if (!cancelado) temporizador = setTimeout(medir, INTERVALO_MS)
    }
    medir()
    return () => {
      cancelado = true
      clearTimeout(temporizador)
    }
  }, [videoRef, activo])

  // Se deriva en cada render, sin resetear estado desde el efecto: cuando la cámara se apaga
  // el último valor medido deja de importar y el indicador vuelve a "sin-señal" de inmediato.
  const nivel: NivelIluminacion =
    !activo || brillo === null
      ? 'sin-señal'
      : brillo < UMBRAL_BAJO
        ? 'oscuro'
        : brillo > UMBRAL_ALTO
          ? 'brillante'
          : 'buena'

  return { brillo: activo ? brillo : null, nivel }
}
