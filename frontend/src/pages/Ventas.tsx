import { useQuery } from '@tanstack/react-query'
import DataTable from '../components/DataTable'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getProductos, getSedes, getVentas } from '../services/api'

export default function Ventas() {
  const ventas = useQuery({ queryKey: ['ventas'], queryFn: getVentas })
  const sedes = useQuery({ queryKey: ['sedes'], queryFn: getSedes })
  const productos = useQuery({ queryKey: ['productos'], queryFn: getProductos })

  const isLoading = ventas.isLoading || sedes.isLoading || productos.isLoading
  const isError = ventas.isError || sedes.isError || productos.isError

  const nombreSede = (id: number) => sedes.data?.find((s) => s.id === id)?.nombre ?? '—'
  const nombreProducto = (id: number) => productos.data?.find((p) => p.id === id)?.nombre ?? '—'

  return (
    <div>
      <PageHeader title="Ventas" description="Registro y análisis de cantidades e importes." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={ventas.data?.length === 0}>
        <DataTable
          rows={ventas.data ?? []}
          rowKey={(row) => row.id}
          columns={[
            { header: 'Fecha', cell: (row) => new Date(row.fecha).toLocaleDateString('es-PE') },
            { header: 'Sucursal', cell: (row) => nombreSede(row.sedeId) },
            { header: 'Producto', cell: (row) => nombreProducto(row.productoId) },
            { header: 'Cantidad', cell: (row) => row.cantidad },
            {
              header: 'Importe',
              cell: (row) => row.importe.toLocaleString('es-PE', { style: 'currency', currency: 'PEN' }),
            },
          ]}
        />
      </QueryState>
    </div>
  )
}
