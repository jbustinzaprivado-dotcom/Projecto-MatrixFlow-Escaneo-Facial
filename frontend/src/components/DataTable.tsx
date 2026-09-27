interface Column<T> {
  header: string
  cell: (row: T) => React.ReactNode
  className?: string
}

interface Props<T> {
  rows: T[]
  columns: Column<T>[]
  rowKey: (row: T) => string | number
}

/** Tabla simple y reutilizable, con desplazamiento horizontal en móvil [PDF §8.5]. */
export default function DataTable<T>({ rows, columns, rowKey }: Props<T>) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white shadow-sm">
      <table className="w-full min-w-max text-left text-sm">
        <thead className="border-b border-slate-200 bg-slate-50 text-xs text-muted uppercase">
          <tr>
            {columns.map((col) => (
              <th key={col.header} className="px-4 py-3 font-semibold">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {rows.map((row) => (
            <tr key={rowKey(row)} className="hover:bg-slate-50">
              {columns.map((col) => (
                <td key={col.header} className={`px-4 py-3 ${col.className ?? ''}`}>
                  {col.cell(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
