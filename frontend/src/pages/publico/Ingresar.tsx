import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'
import VerificacionPanel from '../../components/VerificacionPanel'

// [Añadido D5, D6] Ingreso por DNI + verificación facial 1:1. Desde el feedback del
// instructor, la lógica real vive en VerificacionPanel (reutilizada también por el modal de
// la Landing) — esta página solo aporta el "chrome" específico de ruta completa: el link de
// volver, el encabezado y el ancho fijo. Sigue existiendo porque RutaProtegida redirige aquí
// cuando una sesión expira dentro de una ruta protegida.
export default function Ingresar() {
  return (
    <div className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center px-4 py-10">
      <Link to="/" className="mb-6 inline-flex items-center gap-1 text-sm text-muted hover:text-ink">
        <ArrowLeft size={14} /> Volver al inicio
      </Link>

      <div className="mb-8 text-center">
        <div className="text-xl font-semibold text-ink">MatrixFlow</div>
        <div className="text-sm text-muted">Ingreso por DNI + verificación facial</div>
      </div>

      <VerificacionPanel />
    </div>
  )
}
