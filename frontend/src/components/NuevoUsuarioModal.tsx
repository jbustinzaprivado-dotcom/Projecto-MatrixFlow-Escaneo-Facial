import { isAxiosError } from 'axios'
import { useEffect, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { ScanFace, X } from 'lucide-react'
import IluminacionIndicador from './IluminacionIndicador'
import { useBrillo } from '../hooks/useBrillo'
import { crearUsuario, getSedes, registrarRostro } from '../services/api'
import { capturarFrame } from '../utils/capturarFrame'
import type { Rol, Usuario } from '../types/domain'

type Paso = 'datos' | 'rostro' | 'listo'

interface Props {
  onClose: () => void
  onCreado: () => void
}

/** [Añadido, Fase A] Alta de usuario + registro de rostro, en dos pasos. No existía en la
 * Fase 1 (Usuarios.tsx era solo de lectura): ahora hace falta un flujo real de captura,
 * porque sin un rostro guardado nadie puede verificarse en /ingresar. */
export default function NuevoUsuarioModal({ onClose, onCreado }: Props) {
  const [paso, setPaso] = useState<Paso>('datos')
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  const { data: sedes } = useQuery({ queryKey: ['sedes'], queryFn: getSedes })
  const [form, setForm] = useState({ nombre: '', email: '', dni: '', rol: 'consulta' as Rol, sedeId: 1 })

  const videoRef = useRef<HTMLVideoElement>(null)
  const [camaraActiva, setCamaraActiva] = useState(false)
  const [errorCamara, setErrorCamara] = useState<string | null>(null)
  const { nivel } = useBrillo(videoRef, camaraActiva)

  useEffect(() => {
    if (paso !== 'rostro') return
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
      .catch(() => setErrorCamara('No se pudo acceder a la cámara.'))
    return () => {
      cancelado = true
      setCamaraActiva(false)
      stream?.getTracks().forEach((t) => t.stop())
    }
  }, [paso])

  function mensajeError(e: unknown): string {
    if (isAxiosError(e) && typeof e.response?.data?.detail === 'string') return e.response.data.detail
    return 'Ocurrió un error. Intenta de nuevo.'
  }

  async function crear() {
    setEnviando(true)
    setError(null)
    try {
      const creado = await crearUsuario(form)
      setUsuario(creado)
      setPaso('rostro')
    } catch (e) {
      setError(mensajeError(e))
    } finally {
      setEnviando(false)
    }
  }

  async function capturarYGuardar() {
    if (!videoRef.current || !usuario) return
    setEnviando(true)
    setError(null)
    try {
      const foto = await capturarFrame(videoRef.current)
      await registrarRostro(usuario.id, foto)
      setPaso('listo')
      onCreado()
    } catch (e) {
      setError(mensajeError(e))
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-ink">Nuevo usuario</h2>
          <button type="button" onClick={onClose} aria-label="Cerrar" className="text-muted">
            <X size={20} />
          </button>
        </div>

        {paso === 'datos' && (
          <div className="space-y-3">
            <input
              placeholder="Nombre completo"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            />
            <input
              placeholder="Correo"
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            />
            <input
              placeholder="DNI (8 dígitos)"
              inputMode="numeric"
              maxLength={8}
              value={form.dni}
              onChange={(e) => setForm({ ...form, dni: e.target.value.replace(/\D/g, '') })}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            />
            <select
              value={form.rol}
              onChange={(e) => setForm({ ...form, rol: e.target.value as Rol })}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="administrador">Administrador</option>
              <option value="analista">Analista</option>
              <option value="consulta">Consulta</option>
            </select>
            <select
              value={form.sedeId}
              onChange={(e) => setForm({ ...form, sedeId: Number(e.target.value) })}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              {sedes?.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.nombre}
                </option>
              ))}
            </select>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <button
              type="button"
              onClick={crear}
              disabled={enviando || !form.nombre || !form.email || form.dni.length !== 8}
              className="w-full rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
            >
              {enviando ? 'Creando…' : 'Continuar a captura de rostro'}
            </button>
          </div>
        )}

        {paso === 'rostro' && (
          <div className="space-y-3">
            <p className="text-sm text-muted">Usuario creado. Ahora captura su rostro.</p>
            <div className="overflow-hidden rounded-md bg-sidebar">
              {errorCamara ? (
                <div className="p-6 text-center text-sm text-red-300">{errorCamara}</div>
              ) : (
                <video ref={videoRef} autoPlay playsInline muted className="w-full -scale-x-100" />
              )}
            </div>
            <IluminacionIndicador nivel={nivel} />
            {error && <p className="text-sm text-red-600">{error}</p>}
            <button
              type="button"
              onClick={capturarYGuardar}
              disabled={enviando || !!errorCamara}
              className="flex w-full items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
            >
              <ScanFace size={16} />
              {enviando ? 'Guardando…' : 'Capturar y guardar rostro'}
            </button>
          </div>
        )}

        {paso === 'listo' && (
          <div className="space-y-3 text-center">
            <p className="text-emerald-700">Usuario y rostro guardados correctamente.</p>
            <button
              type="button"
              onClick={onClose}
              className="w-full rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
            >
              Cerrar
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
