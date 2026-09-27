import { useState } from 'react'

interface Tab {
  id: string
  label: string
  content: React.ReactNode
}

/** [Añadido D5] Pestañas para separar secciones dentro de un mismo módulo, así no se carga
 * todo de una vez (p. ej. Historial u Auditoría, con muchas filas). Cada pestaña monta su
 * contenido recién cuando se abre por primera vez. */
export default function Tabs({ tabs, initial }: { tabs: Tab[]; initial?: string }) {
  const [active, setActive] = useState(initial ?? tabs[0]?.id)
  const [opened, setOpened] = useState<Set<string>>(new Set([initial ?? tabs[0]?.id]))

  function select(id: string) {
    setActive(id)
    setOpened((prev) => new Set(prev).add(id))
  }

  return (
    <div>
      <div role="tablist" className="mb-4 flex gap-1 border-b border-slate-200">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            type="button"
            aria-selected={active === tab.id}
            onClick={() => select(tab.id)}
            className={`-mb-px border-b-2 px-4 py-2 text-sm font-medium transition-colors ${
              active === tab.id
                ? 'border-primary text-primary'
                : 'border-transparent text-muted hover:text-ink'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {tabs.map((tab) => (
        <div key={tab.id} hidden={active !== tab.id}>
          {opened.has(tab.id) ? tab.content : null}
        </div>
      ))}
    </div>
  )
}
