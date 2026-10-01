import { clsx } from 'clsx'
import type { LucideIcon } from 'lucide-react'
import { twMerge } from 'tailwind-merge'
import { ACCENT_BORDER, type AccentColor } from './AccentCard'

interface Props {
  label: string
  value: string
  icon: LucideIcon
  accent?: AccentColor
}

// [Añadido] `accent` es opcional: sin él, se ve exactamente igual que antes.
export default function StatCard({ label, value, icon: Icon, accent }: Props) {
  return (
    <div
      className={twMerge(
        clsx(
          'flex items-center gap-4 rounded-lg border border-slate-200 bg-white p-6 shadow-sm',
          accent && 'border-l-4',
          accent && ACCENT_BORDER[accent],
        ),
      )}
    >
      <div className="rounded-md bg-primary/10 p-2 text-primary">
        <Icon size={20} />
      </div>
      <div>
        <div className="text-xs text-muted">{label}</div>
        <div className="text-xl font-semibold text-ink">{value}</div>
      </div>
    </div>
  )
}
