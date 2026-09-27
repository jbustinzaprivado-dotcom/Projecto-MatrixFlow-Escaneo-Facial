import { useQuery } from '@tanstack/react-query'
import { QRCodeSVG } from 'qrcode.react'
import { useParams } from 'react-router-dom'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getCarnet } from '../services/api'

const ROL_LABEL = { administrador: 'Administrador', analista: 'Analista', consulta: 'Consulta' }

// [Añadido D8] Carnet solo con datos + código QR del DNI. Nunca lleva foto: el sistema no
// guarda ninguna imagen de las personas.
export default function Carnet() {
  const { id } = useParams<{ id: string }>()
  const usuarioId = Number(id)
  const { data, isLoading, isError } = useQuery({
    queryKey: ['carnet', usuarioId],
    queryFn: () => getCarnet(usuarioId),
    enabled: Number.isFinite(usuarioId),
  })

  return (
    <div>
      <PageHeader title="Carnet" description="Datos del trabajador y código QR con su DNI." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data === null}>
        {data && (
          <div className="max-w-sm overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="bg-sidebar px-5 py-3 text-sm font-semibold text-white">
              MatrixFlow Enterprise
            </div>
            <div className="flex items-center gap-4 p-5">
              <QRCodeSVG value={data.dni} size={96} />
              <div>
                <div className="text-lg font-semibold text-ink">{data.nombre}</div>
                <div className="text-sm text-muted">DNI {data.dni}</div>
                <div className="mt-1 text-sm text-muted">{ROL_LABEL[data.rol]}</div>
                <div className="text-sm text-muted">Sede: {data.sede}</div>
                <div className="text-xs text-muted">
                  Registrado el {new Date(data.creado_en).toLocaleString('es-PE')}
                </div>
                <span
                  className={`mt-2 inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
                    data.activo ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-muted'
                  }`}
                >
                  {data.activo ? 'Activo' : 'Inactivo'}
                </span>
              </div>
            </div>
          </div>
        )}
      </QueryState>
    </div>
  )
}
