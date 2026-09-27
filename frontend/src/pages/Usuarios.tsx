import { useQuery, useQueryClient } from '@tanstack/react-query'
import { IdCard, UserPlus } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import DataTable from '../components/DataTable'
import NuevoUsuarioModal from '../components/NuevoUsuarioModal'
import PageHeader from '../components/PageHeader'
import QueryState from '../components/QueryState'
import { useAuth } from '../context/AuthContext'
import { getUsuarios } from '../services/api'

const ROL_LABEL = { administrador: 'Administrador', analista: 'Analista', consulta: 'Consulta' }

export default function Usuarios() {
  const queryClient = useQueryClient()
  const { usuario } = useAuth()
  const esAdministrador = usuario?.rol === 'administrador'
  const [modalAbierto, setModalAbierto] = useState(false)
  const { data, isLoading, isError } = useQuery({ queryKey: ['usuarios'], queryFn: getUsuarios })

  return (
    <div>
      <PageHeader title="Usuarios" description="Cuentas del sistema, roles e ingreso por DNI.">
        {/* [Añadido, Fase 6, D71] alta de usuarios: solo administrador (el backend también lo exige) */}
        {esAdministrador && (
          <button
            type="button"
            onClick={() => setModalAbierto(true)}
            className="flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
          >
            <UserPlus size={16} /> Nuevo usuario
          </button>
        )}
      </PageHeader>

      <QueryState isLoading={isLoading} isError={isError} isEmpty={data?.length === 0}>
        <DataTable
          rows={data ?? []}
          rowKey={(row) => row.id}
          columns={[
            { header: 'Nombre', cell: (row) => row.nombre },
            { header: 'Correo', cell: (row) => row.email },
            { header: 'DNI', cell: (row) => row.dni },
            { header: 'Rol', cell: (row) => ROL_LABEL[row.rol] },
            {
              header: 'Estado',
              cell: (row) => (
                <span
                  className={
                    row.activo
                      ? 'rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700'
                      : 'rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-muted'
                  }
                >
                  {row.activo ? 'Activo' : 'Inactivo'}
                </span>
              ),
            },
            {
              header: 'Carnet',
              cell: (row) => (
                <Link
                  to={`/usuarios/${row.id}/carnet`}
                  className="inline-flex items-center gap-1 text-sm font-medium text-primary hover:underline"
                >
                  <IdCard size={14} /> Ver carnet
                </Link>
              ),
            },
          ]}
        />
      </QueryState>

      {modalAbierto && (
        <NuevoUsuarioModal
          onClose={() => setModalAbierto(false)}
          onCreado={() => queryClient.invalidateQueries({ queryKey: ['usuarios'] })}
        />
      )}
    </div>
  )
}
