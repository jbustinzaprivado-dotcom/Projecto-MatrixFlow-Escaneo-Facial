import { useQuery } from '@tanstack/react-query'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getVectores } from '../services/api'

export default function Vectores() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['vectores'], queryFn: getVectores })

  return (
    <div>
      <PageHeader
        title="Vectores"
        description="Representación de información empresarial unidimensional."
      />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {data?.map((vector) => {
            const puntos = vector.valores.map((valor, i) => ({ componente: `v${i + 1}`, valor }))
            return (
              <div key={vector.id} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
                <div className="mb-1 text-sm font-semibold text-ink">{vector.nombre}</div>
                <div className="mb-3 text-xs text-muted">{vector.origen}</div>
                {/* [Añadido] Antes eran barras CSS de 64px sin ejes ni tooltip; con recharts se
                    aprovecha el espacio libre de la tarjeta y se puede leer cada componente. */}
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={puntos}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="componente" fontSize={12} />
                    <YAxis fontSize={12} />
                    <Tooltip />
                    <Bar dataKey="valor" fill="#7c3aed" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
                <div className="mt-2 font-mono text-xs text-muted">
                  [{vector.valores.join(', ')}]
                </div>
              </div>
            )
          })}
        </div>
      </QueryState>
    </div>
  )
}
