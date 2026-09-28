import { useQuery } from '@tanstack/react-query'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getMatrices } from '../services/api'

// [Añadido] Mapa de calor: cada celda se colorea según su magnitud relativa al resto de la
// misma matriz, para detectar de un vistazo la sede/producto que más pesa, en vez de tener
// que leer cada número por separado en una tabla plana.
function colorCelda(valor: number, min: number, max: number): string {
  const t = max === min ? 0.5 : (valor - min) / (max - min)
  const alpha = 0.12 + t * 0.75
  return `rgba(37, 99, 235, ${alpha.toFixed(2)})`
}

export default function Matrices() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['matrices'], queryFn: getMatrices })

  return (
    <div>
      <PageHeader title="Matrices" description="Representación de información multidimensional." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <div className="space-y-6">
          {data?.map((matriz) => {
            const plano = matriz.valores.flat()
            const min = Math.min(...plano)
            const max = Math.max(...plano)
            return (
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
                              style={{ backgroundColor: colorCelda(valor, min, max) }}
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
            )
          })}
        </div>
      </QueryState>
    </div>
  )
}
