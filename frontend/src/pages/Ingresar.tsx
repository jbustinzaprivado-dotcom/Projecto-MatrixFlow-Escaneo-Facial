import { isAxiosError } from 'axios'
import { ArrowLeft, ScanFace } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import CarnetCard from '../components/CarnetCard'
import IluminacionIndicador from '../components/IluminacionIndicador'
import { useAuth } from '../context/AuthContext'
import { useBrillo } from '../hooks/useBrillo'
import { verificarPorDni } from '../services/api'
import { capturarFrame } from '../utils/capturarFrame'
import type { VerificacionResultado } from '../types/domain'

type Paso = 'formulario' | 'resultado'

// [Añadido D5, D6] Ingreso por DNI + verificación facial 1:1: el DNI busca al usuario exacto
// y la cámara solo confirma que es él (no se compara contra todos los usuarios). Desde la
// Fase 6, al coincidir también abre la sesión real del sistema (D70, corrige D44).
//
// [Añadido, feedback del equipo] La cámara y el campo de DNI se muestran juntos desde el
// principio (antes eran dos pasos separados, uno detrás del otro, que se veían muy vacíos
// por separado) — y el carnet, al coincidir, aparece en la misma pantalla en vez de exigir
// un clic aparte a otra página.
export default function Ingresar() {
  const { login } = useAuth()
  const [paso, setPaso] = useState<Paso>('formulario')
  const [dni, setDni] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [verificando, setVerificando] = useState(false)
  const [resultado, setResultado] = useState<VerificacionResultado | null>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const [camaraActiva, setCamaraActiva] = useState(false)
  const [errorCamara, setErrorCamara] = useState<string | null>(null)
  const { nivel } = useBrillo(videoRef, camaraActiva)

  const dniValido = /^\d{8}$/.test(dni)

  useEffect(() => {
    if (paso !== 'formulario') return
    let stream: MediaStream | null = null
    let cancelado = false

    navigator.mediaDevices
      ?.getUserMedia({ video: { facingMode: 'user' } })
      .then((s) => {
        if (cancelado) {
          s.getTracks().forEach((t) => t.stop())
          return
        }
        stream = s
        if (videoRef.current) videoRef.current.srcObject = s
        setCamaraActiva(true)
      })
      .catch(() => setErrorCamara('No se pudo acceder a la cámara. Revisa los permisos del navegador.'))

    return () => {
      cancelado = true
      setCamaraActiva(false)
      stream?.getTracks().forEach((t) => t.stop())
    }
  }, [paso])

  async function verificar() {
    if (!videoRef.current || !dniValido) return
    setVerificando(true)
    setError(null)
    try {
      const foto = await capturarFrame(videoRef.current)
      const respuesta = await verificarPorDni(dni, foto)
      if (respuesta.coincide && respuesta.usuario && respuesta.token) {
        login(respuesta.token, respuesta.usuario)
      }
      setResultado(respuesta)
      setPaso('resultado')
    } catch (e) {
      if (isAxiosError(e) && typeof e.response?.data?.detail === 'string') {
        setError(e.response.data.detail)
      } else {
        setError('No se pudo verificar el rostro. Intenta de nuevo.')
      }
    } finally {
      setVerificando(false)
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center px-4 py-10">
      <Link to="/" className="mb-6 inline-flex items-center gap-1 text-sm text-muted hover:text-ink">
        <ArrowLeft size={14} /> Volver al inicio
      </Link>

      <div className="mb-8 text-center">
        <div className="text-xl font-semibold text-ink">MatrixFlow Enterprise</div>
        <div className="text-sm text-muted">Ingreso por DNI + verificación facial</div>
      </div>

      {paso === 'formulario' && (
        <div className="grid grid-cols-1 gap-6 rounded-lg border border-slate-200 bg-white p-6 shadow-sm md:grid-cols-2">
          <div className="flex flex-col justify-center gap-4">
            <div>
              <label className="mb-1 block text-sm font-medium text-ink" htmlFor="dni">
                DNI
              </label>
              <input
                id="dni"
                inputMode="numeric"
                maxLength={8}
                value={dni}
                onChange={(e) => setDni(e.target.value.replace(/\D/g, ''))}
                placeholder="Ingresa tus 8 dígitos"
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              />
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <button
              type="button"
              onClick={verificar}
              disabled={!dniValido || verificando || !!errorCamara || !camaraActiva}
              className="flex w-full items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
            >
              <ScanFace size={16} />
              {verificando ? 'Verificando…' : 'Verificar rostro'}
            </button>
            <p className="text-xs text-muted">
              Ingresa tu DNI y muestra tu rostro a la cámara — ambos se validan en un solo paso.
            </p>
          </div>

          <div className="space-y-3">
            <div className="overflow-hidden rounded-md bg-sidebar">
              {errorCamara ? (
                <div className="p-6 text-center text-sm text-red-300">{errorCamara}</div>
              ) : (
                <video ref={videoRef} autoPlay playsInline muted className="w-full -scale-x-100" />
              )}
            </div>
            <IluminacionIndicador nivel={nivel} />
          </div>
        </div>
      )}

      {paso === 'resultado' && resultado && (
        <div className="space-y-4 text-center">
          {resultado.coincide && resultado.usuario ? (
            <>
              <h2 className="text-lg font-semibold text-emerald-700">Identidad verificada</h2>
              <CarnetCard
                nombre={resultado.usuario.nombre}
                dni={resultado.usuario.dni}
                rol={resultado.usuario.rol}
                sede={resultado.usuario.sede}
                activo={resultado.usuario.activo}
                creadoEn={resultado.usuario.creadoEn}
              />
              <Link
                to="/dashboard"
                className="mx-auto inline-flex w-full max-w-sm items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
              >
                Entrar al sistema
              </Link>
            </>
          ) : (
            <div className="mx-auto max-w-sm space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-red-600">No se pudo verificar</h2>
              <p className="text-sm text-muted">
                El DNI no está registrado o el rostro no coincide con los datos guardados.
              </p>
              <button
                type="button"
                onClick={() => {
                  setPaso('formulario')
                  setResultado(null)
                }}
                className="w-full rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-ink"
              >
                Intentar de nuevo
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
