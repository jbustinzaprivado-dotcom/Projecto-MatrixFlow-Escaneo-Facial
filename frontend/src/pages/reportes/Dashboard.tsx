import { useQuery } from '@tanstack/react-query'
import { Boxes, Building2, Calculator, ShoppingCart } from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import PageHeader from '../../components/PageHeader'
import QueryState from '../../components/QueryState'
import StatCard from '../../components/StatCard'
import { getDashboardResumen } from '../../services/api'

const formatoSoles = (v: number) => v.toLocaleString('es-PE', { style: 'currency', currency: 'PEN' })

export default function Dashboard() {
  const { data, isLoading, isError } = useQuery({
    queryKey: ['dashboard-resumen'],
    queryFn: getDashboardResumen,
  })

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Indicadores ejecutivos de ventas, inventario y álgebra lineal."
      />
      <QueryState isLoading={isLoading} isError={isError}>
        {data && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <StatCard label="Sucursales" value={String(data.totalSedes)} icon={Building2} />
              <StatCard label="Productos" value={String(data.totalProductos)} icon={Boxes} />
              <StatCard label="Ventas totales" value={formatoSoles(data.totalVentas)} icon={ShoppingCart} />
              <StatCard
                label="Operaciones ejecutadas"
                value={String(data.operacionesEjecutadas)}
                icon={Calculator}
              />
            </div>

            {/* [Añadido] Tendencia de ventas y comparativo por sede: las 5 tarjetas de arriba
                solo dan un total plano; estos dos gráficos aprovechan el detalle semanal y
                por sucursal que ya vive en la base de datos (D104-D105). */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
                <div className="mb-3 text-sm font-semibold text-ink">Tendencia de ventas (16 semanas)</div>
                <ResponsiveContainer width="100%" height={260}>
                  <LineChart data={data.tendenciaSemanal}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="semana" fontSize={12} />
                    <YAxis fontSize={12} />
                    <Tooltip formatter={(v) => formatoSoles(Number(v))} />
                    <Line type="monotone" dataKey="total" stroke="#2563eb" strokeWidth={2} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
                <div className="mb-3 text-sm font-semibold text-ink">Ventas por sucursal</div>
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={data.ventasPorSede}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="sede" fontSize={12} />
                    <YAxis fontSize={12} />
                    <Tooltip formatter={(v) => formatoSoles(Number(v))} />
                    <Bar dataKey="total" fill="#06b6d4" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </QueryState>
    </div>
  )
}
