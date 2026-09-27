interface Props {
  isLoading: boolean
  isError: boolean
  isEmpty?: boolean
  emptyText?: string
  children: React.ReactNode
}

/** Envoltorio de carga/error/vacío reutilizado en toda la app [Añadido, misma idea que el
 * proyecto de referencia: cada bloque carga y falla por separado]. */
export default function QueryState({ isLoading, isError, isEmpty, emptyText, children }: Props) {
  if (isLoading) {
    return <div className="py-8 text-center text-sm text-muted">Cargando…</div>
  }
  if (isError) {
    return (
      <div className="py-8 text-center text-sm text-red-600">No se pudo cargar la información.</div>
    )
  }
  if (isEmpty) {
    return <div className="py-8 text-center text-sm text-muted">{emptyText ?? 'Sin datos.'}</div>
  }
  return <>{children}</>
}
