import { useQuery } from '@tanstack/react-query'
import { isAxiosError } from 'axios'
import { useState } from 'react'
import PageHeader from '../components/PageHeader'
import { useAuth } from '../context/AuthContext'
import { crearOperacion, getVectores } from '../services/api'
import type { TipoOperacion } from '../types/domain'

type OperacionVector = Extract<
  TipoOperacion,
  'suma_vector' | 'resta_vector' | 'producto_escalar' | 'escalar_vector'
>

// Desde la Fase 5, el cálculo ya no se hace en el navegador (corrige D22): se llama a
// POST /operations, que lo resuelve con NumPy en el servidor (Fase 4, [PDF §11]).
export default function Operaciones() {
  const { usuario } = useAuth()
  // [Añadido, Fase 6, D71] consulta es solo lectura: el backend ya lo exige (403), esto
  // solo evita que intente ejecutar algo que de todas formas va a rechazar.
  const puedeEjecutar = usuario?.rol !== 'consulta'
  const { data: vectores } = useQuery({ queryKey: ['vectores'], queryFn: getVectores })
  const [operacion, setOperacion] = useState<OperacionVector>('suma_vector')
  const [idA, setIdA] = useState<number | null>(null)
  const [idB, setIdB] = useState<number | null>(null)
  const [escalar, setEscalar] = useState(1)
  const [resultado, setResultado] = useState<string | null>(null)
  const [ejecutando, setEjecutando] = useState(false)

  function mensajeError(e: unknown): string {
    if (isAxiosError(e)) {
      const detalle = e.response?.data?.detail
      if (typeof detalle === 'string') return detalle
    }
    return 'No se pudo ejecutar la operación.'
  }

  async function ejecutar() {
    if (idA === null) return
    setEjecutando(true)
    try {
      const op = await crearOperacion({
        tipo: operacion,
        vectorAId: idA,
        vectorBId: operacion !== 'escalar_vector' ? (idB ?? undefined) : undefined,
        escalar: operacion === 'escalar_vector' ? escalar : undefined,
      })
      setResultado(op.resultado)
    } catch (e) {
      setResultado(mensajeError(e))
    } finally {
      setEjecutando(false)
    }
  }

  return (
    <div>
      <PageHeader title="Operaciones" description="Selección y ejecución de cálculos de álgebra lineal." />
      <div className="max-w-xl space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div>
          <label className="mb-1 block text-xs font-medium text-muted" htmlFor="operacion">
            Operación
          </label>
          <select
            id="operacion"
            value={operacion}
            onChange={(e) => setOperacion(e.target.value as OperacionVector)}
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          >
            <option value="suma_vector">Suma de vectores</option>
            <option value="resta_vector">Resta de vectores</option>
            <option value="producto_escalar">Producto escalar (punto)</option>
            <option value="escalar_vector">Multiplicación por escalar</option>
          </select>
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-muted" htmlFor="vectorA">
            Vector A
          </label>
          <select
            id="vectorA"
            value={idA ?? ''}
            onChange={(e) => setIdA(Number(e.target.value) || null)}
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          >
            <option value="">Selecciona un vector</option>
            {vectores?.map((v) => (
              <option key={v.id} value={v.id}>
                {v.nombre}
              </option>
            ))}
          </select>
        </div>

        {operacion !== 'escalar_vector' ? (
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="vectorB">
              Vector B
            </label>
            <select
              id="vectorB"
              value={idB ?? ''}
              onChange={(e) => setIdB(Number(e.target.value) || null)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">Selecciona un vector</option>
              {vectores?.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.nombre}
                </option>
              ))}
            </select>
          </div>
        ) : (
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="escalar">
              Escalar
            </label>
            <input
              id="escalar"
              type="number"
              value={escalar}
              onChange={(e) => setEscalar(Number(e.target.value))}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
        )}

        <button
          type="button"
          onClick={ejecutar}
          disabled={ejecutando || idA === null || !puedeEjecutar}
          className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
        >
          {ejecutando ? 'Calculando…' : 'Ejecutar'}
        </button>
        {!puedeEjecutar && (
          <p className="text-xs text-muted">Tu rol (consulta) solo tiene acceso de lectura.</p>
        )}

        {resultado !== null && (
          <div className="rounded-md bg-slate-50 p-3 font-mono text-sm text-ink">{resultado}</div>
        )}
      </div>
    </div>
  )
}
