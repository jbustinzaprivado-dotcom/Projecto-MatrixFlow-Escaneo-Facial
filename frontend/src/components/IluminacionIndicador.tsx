import type { NivelIluminacion } from '../hooks/useBrillo'

const TEXTO: Record<NivelIluminacion, string> = {
  'sin-señal': 'Esperando la cámara…',
  oscuro: 'Muy oscuro: acércate a una luz.',
  brillante: 'Demasiada luz directa: evita el contraluz.',
  buena: 'Buena iluminación.',
}

const COLOR: Record<NivelIluminacion, string> = {
  'sin-señal': 'bg-slate-300',
  oscuro: 'bg-red-500',
  brillante: 'bg-amber-500',
  buena: 'bg-emerald-500',
}

/** [Añadido D5] Feedback de iluminación en vivo durante la captura del rostro. */
export default function IluminacionIndicador({ nivel }: { nivel: NivelIluminacion }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className={`h-2.5 w-2.5 rounded-full ${COLOR[nivel]}`} />
      <span className="text-muted">{TEXTO[nivel]}</span>
    </div>
  )
}
