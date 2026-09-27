import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { PackagePlus } from 'lucide-react'
import DataTable from '../components/DataTable'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import RegistrarMovimientoModal from '../components/RegistrarMovimientoModal'
import { useAuth } from '../context/AuthContext'
import { getInventario, getProductos, getSedes } from '../services/api'

export default function Inventario() {
  const queryClient = useQueryClient()
  const { usuario } = useAuth()
  const puedeRegistrar = usuario?.rol !== 'consulta' // [RF-06, D71]
  const [modalAbierto, setModalAbierto] = useState(false)
  const inventario = useQuery({ queryKey: ['inventario'], queryFn: getInventario })
  const sedes = useQuery({ queryKey: ['sedes'], queryFn: getSedes })
  const productos = useQuery({ queryKey: ['productos'], queryFn: getProductos })

  const isLoading = inventario.isLoading || sedes.isLoading || productos.isLoading
  const isError = inventario.isError || sedes.isError || productos.isError

  const nombreSede = (id: number) => sedes.data?.find((s) => s.id === id)?.nombre ?? '—'
  const nombreProducto = (id: number) => productos.data?.find((p) => p.id === id)?.nombre ?? '—'

  return (
    <div>
      <PageHeader title="Inventario" description="Existencias y movimientos por sucursal.">
        {puedeRegistrar && (
          <button
            type="button"
            onClick={() => setModalAbierto(true)}
            className="flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
          >
            <PackagePlus size={16} /> Registrar movimiento
          </button>
        )}
      </PageHeader>
      <QueryState isLoading={isLoading} isError={isError} isEmpty={inventario.data?.length === 0}>
        <DataTable
          rows={inventario.data ?? []}
          rowKey={(row) => row.id}
          columns={[
            { header: 'Sucursal', cell: (row) => nombreSede(row.sedeId) },
            { header: 'Producto', cell: (row) => nombreProducto(row.productoId) },
            {
              header: 'Existencias',
              cell: (row) => (
                <span className={row.existencias < 25 ? 'font-medium text-amber-600' : ''}>
                  {row.existencias}
                </span>
              ),
            },
            {
              header: 'Actualizado',
              cell: (row) => new Date(row.actualizadoEn).toLocaleDateString('es-PE'),
            },
          ]}
        />
      </QueryState>

      {modalAbierto && (
        <RegistrarMovimientoModal
          onClose={() => setModalAbierto(false)}
          onRegistrado={() => queryClient.invalidateQueries({ queryKey: ['inventario'] })}
        />
      )}
    </div>
  )
}
