import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import CarnetCard from '../../components/CarnetCard'
import PageHeader from '../../components/PageHeader'
import QueryState from '../../components/QueryState'
import { getCarnet } from '../../services/api'

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
          <CarnetCard
            nombre={data.nombre}
            dni={data.dni}
            rol={data.rol}
            sede={data.sede}
            activo={data.activo}
            creadoEn={data.creado_en}
          />
        )}
      </QueryState>
    </div>
  )
}
