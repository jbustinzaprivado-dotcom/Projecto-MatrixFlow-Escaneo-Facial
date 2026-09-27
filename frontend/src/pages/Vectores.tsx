import { useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getVectores } from '../services/api'

export default function Vectores() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['vectores'], queryFn: getVectores })
  const [seleccionado, setSeleccionado] = useState<number | null>(null)

  return (
    <div>
      <PageHeader
        title="Vectores"
        description="Representación de información empresarial unidimensional."
      />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {data?.map((vector) => {
            const max = Math.max(...vector.valores, 1)
            return (
              <button
                key={vector.id}
                type="button"
                onClick={() => setSeleccionado(vector.id)}
                className={`rounded-lg border bg-white p-4 text-left shadow-sm transition-colors ${
                  seleccionado === vector.id ? 'border-primary' : 'border-slate-200'
                }`}
              >
                <div className="mb-1 text-sm font-semibold text-ink">{vector.nombre}</div>
                <div className="mb-3 text-xs text-muted">{vector.origen}</div>
                <div className="flex items-end gap-1" style={{ height: 64 }}>
                  {vector.valores.map((valor, i) => (
                    <div key={i} className="flex flex-1 flex-col items-center gap-1">
                      <div
                        className="w-full rounded-t bg-primary/70"
                        style={{ height: `${(valor / max) * 48}px` }}
                      />
                      <span className="text-[10px] text-muted">{valor}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-2 font-mono text-xs text-muted">
                  [{vector.valores.join(', ')}]
                </div>
              </button>
            )
          })}
        </div>
      </QueryState>
    </div>
  )
}
