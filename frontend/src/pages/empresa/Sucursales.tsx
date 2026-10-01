import { useQuery } from '@tanstack/react-query'
import DataTable from '../../components/DataTable'
import PageHeader from '../../components/PageHeader'
import QueryState from '../../components/QueryState'
import { getSedes } from '../../services/api'

export default function Sucursales() {
  const { data, isLoading, isError } = useQuery({ queryKey: ['sedes'], queryFn: getSedes })

  return (
    <div>
      <PageHeader title="Sucursales" description="Administración de sedes y datos operativos." />
      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <DataTable
          rows={data ?? []}
          rowKey={(row) => row.id}
          columns={[
            { header: 'Sucursal', cell: (row) => row.nombre },
            { header: 'Departamento', cell: (row) => row.departamento },
            { header: 'Distrito', cell: (row) => row.distrito },
            { header: 'Dirección', cell: (row) => row.direccion },
          ]}
        />
      </QueryState>
    </div>
  )
}
