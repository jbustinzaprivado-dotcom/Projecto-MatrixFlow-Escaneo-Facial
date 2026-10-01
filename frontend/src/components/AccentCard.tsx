import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

// [Añadido] Franja de color a la izquierda, inspirada en las tarjetas de Blackboard — mismo
// shell de tarjeta usado en todo el proyecto (StatCard, DataTable, paneles de Dashboard),
// solo con un borde izquierdo de color. Reutiliza los 2 tokens de marca (primary/accent) más
// 4 colores estándar de Tailwind, sin agregar tokens nuevos a index.css.
export type AccentColor = 'primary' | 'accent' | 'pink' | 'violet' | 'amber' | 'emerald'

export const ACCENT_BORDER: Record<AccentColor, string> = {
  primary: 'border-l-primary',
  accent: 'border-l-accent',
  pink: 'border-l-pink-400',
  violet: 'border-l-violet-400',
  amber: 'border-l-amber-400',
  emerald: 'border-l-emerald-400',
}

interface Props {
  accent: AccentColor
  className?: string
  children: React.ReactNode
}

export default function AccentCard({ accent, className, children }: Props) {
  return (
    <div
      className={twMerge(
        clsx('rounded-lg border border-slate-200 bg-white p-6 shadow-sm border-l-4', ACCENT_BORDER[accent]),
        className,
      )}
    >
      {children}
    </div>
  )
}
