import { isAxiosError } from 'axios'
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { X } from 'lucide-react'
import { getProductos, getSedes, registrarMovimiento } from '../services/api'

interface Props {
  onClose: () => void
  onRegistrado: () => void
}

/** [RF-06, Añadido en el repaso de fidelidad §16-21] Registrar una entrada o salida real de
 * existencias — Inventario.tsx era de solo lectura hasta ahora. */
export default function RegistrarMovimientoModal({ onClose, onRegistrado }: Props) {
  const { data: sedes } = useQuery({ queryKey: ['sedes'], queryFn: getSedes })
  const { data: productos } = useQuery({ queryKey: ['productos'], queryFn: getProductos })

  const [sedeId, setSedeId] = useState<number | null>(null)
  const [productoId, setProductoId] = useState<number | null>(null)
  const [tipo, setTipo] = useState<'entrada' | 'salida'>('entrada')
  const [cantidad, setCantidad] = useState(1)
  const [error, setError] = useState<string | null>(null)
  const [enviando, setEnviando] = useState(false)

  function mensajeError(e: unknown): string {
    if (isAxiosError(e) && typeof e.response?.data?.detail === 'string') return e.response.data.detail
    return 'No se pudo registrar el movimiento.'
  }

  async function enviar() {
    if (sedeId === null || productoId === null) return
    setEnviando(true)
    setError(null)
    try {
      await registrarMovimiento({ sedeId, productoId, tipo, cantidad })
      onRegistrado()
      onClose()
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
          <h2 className="text-lg font-semibold text-ink">Registrar movimiento</h2>
          <button type="button" onClick={onClose} aria-label="Cerrar" className="text-muted">
            <X size={20} />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="sede">
              Sucursal
            </label>
            <select
              id="sede"
              value={sedeId ?? ''}
              onChange={(e) => setSedeId(Number(e.target.value) || null)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">Selecciona</option>
              {sedes?.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.nombre}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="producto">
              Producto
            </label>
            <select
              id="producto"
              value={productoId ?? ''}
              onChange={(e) => setProductoId(Number(e.target.value) || null)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">Selecciona</option>
              {productos?.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nombre}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="mb-1 block text-xs font-medium text-muted" htmlFor="tipo">
                Tipo
              </label>
              <select
                id="tipo"
                value={tipo}
                onChange={(e) => setTipo(e.target.value as 'entrada' | 'salida')}
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              >
                <option value="entrada">Entrada</option>
                <option value="salida">Salida</option>
              </select>
            </div>
            <div>
              <label className="mb-1 block text-xs font-medium text-muted" htmlFor="cantidad">
                Cantidad
              </label>
              <input
                id="cantidad"
                type="number"
                min={1}
                value={cantidad}
                onChange={(e) => setCantidad(Number(e.target.value))}
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              />
            </div>
          </div>

          {error && <p className="text-sm text-red-600">{error}</p>}

          <button
            type="button"
            onClick={enviar}
            disabled={enviando || sedeId === null || productoId === null}
            className="w-full rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          >
            {enviando ? 'Registrando…' : 'Registrar'}
          </button>
        </div>
      </div>
    </div>
  )
}
