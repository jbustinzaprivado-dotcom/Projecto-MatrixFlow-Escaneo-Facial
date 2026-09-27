import type { LucideIcon } from 'lucide-react'

interface Props {
  label: string
  value: string
  icon: LucideIcon
}

export default function StatCard({ label, value, icon: Icon }: Props) {
  return (
    <div className="flex items-center gap-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
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
