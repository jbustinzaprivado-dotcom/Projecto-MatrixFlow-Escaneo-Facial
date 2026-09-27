import { useQuery } from '@tanstack/react-query'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getMatrices } from '../services/api'

export default function Matrices() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['matrices'], queryFn: getMatrices })

  return (
    <div>
      <PageHeader title="Matrices" description="Representación de información multidimensional." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <div className="space-y-6">
          {data?.map((matriz) => (
            <div key={matriz.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <div className="mb-1 text-sm font-semibold text-ink">{matriz.nombre}</div>
              <div className="mb-3 text-xs text-muted">
                {matriz.origen} · {matriz.filas}×{matriz.columnas}
              </div>
              <div className="overflow-x-auto">
                <table className="border-collapse font-mono text-sm">
                  <tbody>
                    {matriz.valores.map((fila, i) => (
                      <tr key={i}>
                        {fila.map((valor, j) => (
                          <td
                            key={j}
                            className="border border-slate-200 px-3 py-1.5 text-center text-ink"
                          >
                            {valor}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      </QueryState>
    </div>
  )
}
