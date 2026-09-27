import { useQuery } from '@tanstack/react-query'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { getEmpresa } from '../services/api'

export default function Empresa() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['empresa'], queryFn: getEmpresa })

  return (
    <div>
      <PageHeader title="Empresa" description="Información corporativa y configuración del negocio." />
      <QueryState isLoading={isLoading} isError={isError}>
        {data && (
          <div className="max-w-xl space-y-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
            <div>
              <div className="text-xs text-muted">Razón social</div>
              <div className="text-sm font-medium text-ink">{data.razonSocial}</div>
            </div>
            <div>
              <div className="text-xs text-muted">RUC</div>
              <div className="text-sm font-medium text-ink">{data.ruc}</div>
            </div>
            <div>
              <div className="text-xs text-muted">Rubro</div>
              <div className="text-sm font-medium text-ink">{data.rubro}</div>
            </div>
          </div>
        )}
      </QueryState>
    </div>
  )
}
