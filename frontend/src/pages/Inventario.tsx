import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { PackagePlus } from 'lucide-react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
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

  // [Añadido] Total de existencias por producto (sumado entre las 5 sedes), para ver de un
  // vistazo qué producto tiene más/menos stock a nivel empresa, antes de bajar a la tabla
  // detallada por sucursal.
  const porProducto = new Map<number, number>()
  for (const item of inventario.data ?? []) {
    porProducto.set(item.productoId, (porProducto.get(item.productoId) ?? 0) + item.existencias)
  }
  const datosGrafico = [...porProducto.entries()].map(([productoId, total]) => ({
    producto: nombreProducto(productoId),
    total,
  }))

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
        <div className="space-y-6">
          <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-3 text-sm font-semibold text-ink">Existencias totales por producto</div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={datosGrafico}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="producto" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip />
                <Bar dataKey="total" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

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
        </div>
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
