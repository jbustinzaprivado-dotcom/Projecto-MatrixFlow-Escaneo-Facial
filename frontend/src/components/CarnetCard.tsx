import { QRCodeSVG } from 'qrcode.react'
import type { Rol } from '../types/domain'

const ROL_LABEL: Record<Rol, string> = {
  administrador: 'Administrador',
  analista: 'Analista',
  consulta: 'Consulta',
}

export interface CarnetCardProps {
  nombre: string
  dni: string
  rol: Rol
  sede: string
  activo: boolean
  creadoEn: string
  /** [Añadido, feedback del instructor] Fecha a mostrar en vez de `creadoEn` — la usa el
   * login biométrico (VerificacionPanel) para mostrar el momento de ESTE ingreso, no la
   * fecha de creación de la cuenta (bug corregido: antes el carnet del login mostraba
   * `usuario.creado_en`, fijo desde el alta de la cuenta). Si se omite, se muestra
   * `creadoEn` — Carnet.tsx no la pasa y sigue mostrando lo mismo que siempre. */
  fechaMostrada?: string
  /** Por defecto "Registrado el" — el mismo texto que Carnet.tsx siempre mostró. */
  etiquetaFecha?: string
}

// [Añadido D8] Carnet solo con datos + código QR del DNI. Nunca lleva foto: el sistema no
// guarda ninguna imagen de las personas. Extraído de Carnet.tsx para reutilizarse también en
// el resultado del login biométrico (VerificacionPanel) — mismo diseño, sin duplicar el JSX.
export default function CarnetCard({
  nombre,
  dni,
  rol,
  sede,
  activo,
  creadoEn,
  fechaMostrada,
  etiquetaFecha = 'Registrado el',
}: CarnetCardProps) {
  return (
    <div className="mx-auto max-w-sm overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <div className="bg-sidebar px-5 py-3 text-sm font-semibold text-white">MatrixFlow</div>
      <div className="flex items-center gap-4 p-5">
        <QRCodeSVG value={dni} size={96} />
        <div>
          <div className="text-lg font-semibold text-ink">{nombre}</div>
          <div className="text-sm text-muted">DNI {dni}</div>
          <div className="mt-1 text-sm text-muted">{ROL_LABEL[rol]}</div>
          <div className="text-sm text-muted">Sede: {sede}</div>
          <div className="text-xs text-muted">
            {etiquetaFecha} {new Date(fechaMostrada ?? creadoEn).toLocaleString('es-PE')}
          </div>
          <span
            className={`mt-2 inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
              activo ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-muted'
            }`}
          >
            {activo ? 'Activo' : 'Inactivo'}
          </span>
        </div>
      </div>
    </div>
  )
}
