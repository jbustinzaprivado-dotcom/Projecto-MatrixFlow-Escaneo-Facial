import { useQuery } from '@tanstack/react-query'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import DataTable from '../../components/DataTable'
import PageHeader from '../../components/PageHeader'
import QueryState from '../../components/QueryState'
import Tabs from '../../components/Tabs'
import { getAuditoria, getAuditoriaResumen } from '../../services/api'
import type { AuditoriaEntry } from '../../types/domain'

function TablaAuditoria({ rows }: { rows: AuditoriaEntry[] }) {
  return (
    <DataTable
      rows={rows}
      rowKey={(row) => row.id}
      columns={[
        { header: 'Fecha', cell: (row) => new Date(row.fecha).toLocaleString('es-PE') },
        { header: 'Usuario', cell: (row) => row.usuario },
        { header: 'Acción', cell: (row) => row.accion },
        { header: 'Recurso', cell: (row) => row.recurso },
        {
          header: 'Resultado',
          cell: (row) => (
            <span
              className={
                row.resultado === 'ok'
                  ? 'rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700'
                  : 'rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700'
              }
            >
              {row.resultado === 'ok' ? 'Correcto' : 'Error'}
            </span>
          ),
        },
        { header: 'Ubicación (sede)', cell: (row) => row.sede },
      ]}
    />
  )
}

// [Añadido D5, D9] Auditoría extendida: actividad de 7 días, usuarios más activos y ubicación
// fija por sede. Con pestañas para no cargar todo el historial completo de una sola vez.
export default function Auditoria() {
  const auditoria = useQuery({ queryKey: ['auditoria'], queryFn: getAuditoria })
  const resumen = useQuery({ queryKey: ['auditoria-resumen'], queryFn: getAuditoriaResumen })

  return (
    <div>
      <PageHeader
        title="Auditoría"
        description="Actividad de los últimos 7 días, usuarios más activos y ubicación del inicio de sesión."
      />

      <QueryState isLoading={resumen.isLoading} isError={resumen.isError}>
        {resumen.data && (
          <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <div className="mb-3 text-sm font-semibold text-ink">
                Actividad de los últimos 7 días ({resumen.data.total7Dias} eventos)
              </div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={resumen.data.actividadPorDia}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis
                    dataKey="dia"
                    fontSize={12}
                    tickFormatter={(v: string) => new Date(v).toLocaleDateString('es-PE', { weekday: 'short' })}
                  />
                  <YAxis fontSize={12} allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="cantidad" fill="#2563eb" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <div className="mb-3 text-sm font-semibold text-ink">Usuarios más activos (7 días)</div>
              <ol className="space-y-2">
                {resumen.data.masActivos.map((item, i) => (
                  <li key={item.usuario} className="flex items-center justify-between text-sm">
                    <span className="text-ink">
                      {i + 1}. {item.usuario}
                    </span>
                    <span className="font-mono text-muted">{item.cantidad}</span>
                  </li>
                ))}
                {resumen.data.masActivos.length === 0 && (
                  <li className="text-sm text-muted">Sin actividad en los últimos 7 días.</li>
                )}
              </ol>
            </div>
          </div>
        )}
      </QueryState>

      <QueryState
        isLoading={auditoria.isLoading}
        isError={auditoria.isError}
        isEmpty={auditoria.data?.length === 0}
      >
        {auditoria.data && (
          <Tabs
            tabs={[
              { id: 'todas', label: `Todas (${auditoria.data.length})`, content: <TablaAuditoria rows={auditoria.data} /> },
              {
                id: 'errores',
                label: `Errores (${auditoria.data.filter((r) => r.resultado === 'error').length})`,
                content: <TablaAuditoria rows={auditoria.data.filter((r) => r.resultado === 'error')} />,
              },
            ]}
          />
        )}
      </QueryState>
    </div>
  )
}
