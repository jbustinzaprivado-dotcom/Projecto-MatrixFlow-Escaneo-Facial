import { useQuery } from '@tanstack/react-query'
import DataTable from '../components/DataTable'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import Tabs from '../components/Tabs'
import { getHistorial } from '../services/api'
import type { OperacionHistorial } from '../types/domain'

const ETIQUETAS: Record<OperacionHistorial['tipo'], string> = {
  suma_vector: 'Suma de vectores',
  resta_vector: 'Resta de vectores',
  escalar_vector: 'Escalar (vector)',
  producto_escalar: 'Producto escalar',
  suma_matriz: 'Suma de matrices',
  resta_matriz: 'Resta de matrices',
  multiplicacion_matriz: 'Multiplicación de matrices',
  transpuesta_matriz: 'Transpuesta',
  escalar_matriz: 'Escalar (matriz)',
  combinacion_lineal: 'Combinación lineal',
}

function Tabla({ rows }: { rows: OperacionHistorial[] }) {
  return (
    <DataTable
      rows={rows}
      rowKey={(row) => row.id}
      columns={[
        { header: 'Fecha', cell: (row) => new Date(row.fecha).toLocaleString('es-PE') },
        { header: 'Operación', cell: (row) => ETIQUETAS[row.tipo] },
        { header: 'Entradas', cell: (row) => row.entradas },
        { header: 'Resultado', cell: (row) => row.resultado },
        { header: 'Usuario', cell: (row) => row.usuario },
        {
          header: 'Estado',
          cell: (row) => {
            const estilos = {
              ok: 'bg-emerald-100 text-emerald-700',
              error: 'bg-red-100 text-red-700',
              pendiente: 'bg-amber-100 text-amber-700',
            } as const
            const etiquetas = { ok: 'Correcto', error: 'Error', pendiente: 'Pendiente' } as const
            return (
              <span
                className={`rounded-full px-2 py-0.5 text-xs font-medium ${estilos[row.estado]}`}
              >
                {etiquetas[row.estado]}
              </span>
            )
          },
        },
      ]}
    />
  )
}

// [Añadido D5] Pestañas para no cargar todo el historial de una sola vez.
export default function Historial() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['historial'], queryFn: getHistorial })

  return (
    <div>
      <PageHeader title="Historial" description="Trazabilidad de cálculos y resultados." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        {data && (
          <Tabs
            tabs={[
              { id: 'todas', label: `Todas (${data.length})`, content: <Tabla rows={data} /> },
              {
                id: 'ok',
                label: `Correctas (${data.filter((r) => r.estado === 'ok').length})`,
                content: <Tabla rows={data.filter((r) => r.estado === 'ok')} />,
              },
              {
                id: 'error',
                label: `Con error (${data.filter((r) => r.estado === 'error').length})`,
                content: <Tabla rows={data.filter((r) => r.estado === 'error')} />,
              },
              {
                id: 'pendiente',
                label: `Pendientes (${data.filter((r) => r.estado === 'pendiente').length})`,
                content: <Tabla rows={data.filter((r) => r.estado === 'pendiente')} />,
              },
            ]}
          />
        )}
      </QueryState>
    </div>
  )
}
