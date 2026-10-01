import { useQuery } from '@tanstack/react-query'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import AccentCard from '../../components/AccentCard'
import DataTable from '../../components/DataTable'
import MapaUbicaciones from '../../components/MapaUbicaciones'
import PageHeader from '../../components/PageHeader'
import QueryState from '../../components/QueryState'
import Tabs from '../../components/Tabs'
import { useAuth } from '../../context/AuthContext'
import { getAuditoria, getAuditoriaResumen, getUbicacionesActivas } from '../../services/api'
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
  const { usuario } = useAuth()
  const esAdministrador = usuario?.rol === 'administrador'
  const auditoria = useQuery({ queryKey: ['auditoria'], queryFn: getAuditoria })
  const resumen = useQuery({ queryKey: ['auditoria-resumen'], queryFn: getAuditoriaResumen })
  // [Añadido, corrige D9] mapa en vivo (D128): `enabled` evita que un no-administrador
  // dispare el GET, además del RequireAdmin que ya lo bloquea en el backend (D131).
  const ubicaciones = useQuery({
    queryKey: ['ubicaciones-activas'],
    queryFn: getUbicacionesActivas,
    enabled: esAdministrador,
    refetchInterval: 60_000,
  })

  return (
    <div>
      <PageHeader
        title="Auditoría"
        description="Actividad de los últimos 7 días, usuarios más activos y ubicación del inicio de sesión."
      />

      <QueryState isLoading={resumen.isLoading} isError={resumen.isError}>
        {resumen.data && (
          <div className="mb-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
            <AccentCard accent="violet">
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
            </AccentCard>

            <AccentCard accent="amber">
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
            </AccentCard>
          </div>
        )}
      </QueryState>

      {esAdministrador && (
        <AccentCard accent="emerald" className="mb-6">
          <div className="mb-3 text-sm font-semibold text-ink">
            Usuarios activos ahora{ubicaciones.data ? ` (${ubicaciones.data.length})` : ''}
          </div>
          <QueryState isLoading={ubicaciones.isLoading} isError={ubicaciones.isError}>
            {ubicaciones.data && ubicaciones.data.length > 0 ? (
              <MapaUbicaciones ubicaciones={ubicaciones.data} />
            ) : (
              <div className="py-8 text-center text-sm text-muted">
                Nadie tiene una sesión activa en este momento.
              </div>
            )}
          </QueryState>
        </AccentCard>
      )}

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
