import { useQuery } from '@tanstack/react-query'
import DataTable from '../components/DataTable'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getProductos } from '../services/api'

export default function Productos() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['productos'], queryFn: getProductos })

  return (
    <div>
      <PageHeader title="Productos" description="Catálogo, categorías y variables de análisis." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <DataTable
          rows={data ?? []}
          rowKey={(row) => row.id}
          columns={[
            { header: 'Producto', cell: (row) => row.nombre },
            { header: 'Categoría', cell: (row) => row.categoria },
            {
              header: 'Precio',
              cell: (row) => row.precio.toLocaleString('es-PE', { style: 'currency', currency: 'PEN' }),
            },
          ]}
        />
      </QueryState>
    </div>
  )
}
