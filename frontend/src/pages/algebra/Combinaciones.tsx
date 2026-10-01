import { useQuery } from '@tanstack/react-query'
import { isAxiosError } from 'axios'
import { useState } from 'react'
import PageHeader from '../../components/PageHeader'
import { useAuth } from '../../context/AuthContext'
import { crearOperacion, getVectores } from '../../services/api'

// Indicador ponderado de ventas, rentabilidad y rotación [PDF §5]: combinación lineal
// c1*v1 + c2*v2. Desde la Fase 5 la calcula el backend (POST /operations), no el navegador.
export default function Combinaciones() {
  const { usuario } = useAuth()
  const puedeEjecutar = usuario?.rol !== 'consulta' // [Añadido, Fase 6, D71]
  const { data: vectores } = useQuery({ queryKey: ['vectores'], queryFn: getVectores })
  const [idA, setIdA] = useState<number | null>(null)
  const [idB, setIdB] = useState<number | null>(null)
  const [c1, setC1] = useState(1)
  const [c2, setC2] = useState(1)
  const [resultado, setResultado] = useState<string | null>(null)
  const [ejecutando, setEjecutando] = useState(false)

  function mensajeError(e: unknown): string {
    if (isAxiosError(e)) {
      const detalle = e.response?.data?.detail
      if (typeof detalle === 'string') return detalle
    }
    return 'No se pudo ejecutar la combinación.'
  }

  async function ejecutar() {
    if (idA === null || idB === null) return
    setEjecutando(true)
    try {
      const op = await crearOperacion({
        tipo: 'combinacion_lineal',
        vectorAId: idA,
        vectorBId: idB,
        coeficienteA: c1,
        coeficienteB: c2,
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
      <PageHeader
        title="Combinaciones lineales"
        description="Indicador empresarial ponderado a partir de dos vectores."
      />
      <div className="max-w-xl space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="c1">
              Coeficiente c1
            </label>
            <input
              id="c1"
              type="number"
              value={c1}
              onChange={(e) => setC1(Number(e.target.value))}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="vA">
              Vector A
            </label>
            <select
              id="vA"
              value={idA ?? ''}
              onChange={(e) => setIdA(Number(e.target.value) || null)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">Selecciona</option>
              {vectores?.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.nombre}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="c2">
              Coeficiente c2
            </label>
            <input
              id="c2"
              type="number"
              value={c2}
              onChange={(e) => setC2(Number(e.target.value))}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-muted" htmlFor="vB">
              Vector B
            </label>
            <select
              id="vB"
              value={idB ?? ''}
              onChange={(e) => setIdB(Number(e.target.value) || null)}
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">Selecciona</option>
              {vectores?.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.nombre}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          type="button"
          onClick={ejecutar}
          disabled={ejecutando || idA === null || idB === null || !puedeEjecutar}
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
