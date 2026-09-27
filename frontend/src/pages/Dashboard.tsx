import { useQuery } from '@tanstack/react-query'
import { Boxes, Building2, Calculator, ShoppingCart } from 'lucide-react'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import StatCard from '../components/StatCard'
import { getDashboardResumen } from '../services/api'

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
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard label="Sucursales" value={String(data.totalSedes)} icon={Building2} />
            <StatCard label="Productos" value={String(data.totalProductos)} icon={Boxes} />
            <StatCard
              label="Ventas totales"
              value={data.totalVentas.toLocaleString('es-PE', { style: 'currency', currency: 'PEN' })}
              icon={ShoppingCart}
            />
            <StatCard
              label="Operaciones ejecutadas"
              value={String(data.operacionesEjecutadas)}
              icon={Calculator}
            />
          </div>
        )}
      </QueryState>
    </div>
  )
}
