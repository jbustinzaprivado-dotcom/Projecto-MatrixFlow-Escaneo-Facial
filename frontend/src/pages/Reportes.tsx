import { useQuery } from '@tanstack/react-query'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getReportes } from '../services/api'

// Desde la Fase 5, el backend agrega con SQL (GET /reports); el navegador ya no recalcula
// nada a partir de ventas/sedes/productos por separado.
export default function Reportes() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['reportes'], queryFn: getReportes })

  return (
    <div>
      <PageHeader title="Reportes" description="Indicadores y gráficos de ventas por sucursal y producto." />
      <QueryState isLoading={isLoading} isError={isError}>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-3 text-sm font-semibold text-ink">Ventas por sucursal</div>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={data?.ventasPorSucursal}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="sucursal" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip
                  formatter={(v) => Number(v).toLocaleString('es-PE', { style: 'currency', currency: 'PEN' })}
                />
                <Bar dataKey="importe" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-3 text-sm font-semibold text-ink">Unidades vendidas por producto</div>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={data?.ventasPorProducto}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="producto" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip />
                <Bar dataKey="cantidad" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </QueryState>
    </div>
  )
}
