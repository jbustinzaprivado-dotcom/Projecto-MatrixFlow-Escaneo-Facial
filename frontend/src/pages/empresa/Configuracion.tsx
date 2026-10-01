import { useQuery } from '@tanstack/react-query'
import DataTable from '../../components/DataTable'
import PageHeader from '../../components/PageHeader'
import QueryState from '../../components/QueryState'
import { getSedes } from '../../services/api'

// [Añadido D9] cada sede lleva su ubicación fija, la misma que usa la auditoría del login.
export default function Configuracion() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['sedes'], queryFn: getSedes })

  return (
    <div>
      <PageHeader
        title="Configuración"
        description="Parámetros del sistema y ubicación fija de cada sede (usada por la auditoría)."
      />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <DataTable
          rows={data ?? []}
          rowKey={(row) => row.id}
          columns={[
            { header: 'Sede', cell: (row) => row.nombre },
            { header: 'Departamento', cell: (row) => row.departamento },
            { header: 'Distrito', cell: (row) => row.distrito },
            { header: 'Dirección', cell: (row) => row.direccion },
          ]}
        />
      </QueryState>
    </div>
  )
}
