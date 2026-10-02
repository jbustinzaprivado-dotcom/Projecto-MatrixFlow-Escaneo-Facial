import { X } from 'lucide-react'
import { useEffect, useState } from 'react'
import VerificacionPanel from './VerificacionPanel'

interface Props {
  onClose: () => void
}

// [Añadido, feedback del instructor] Panel lateral que emerge desde la derecha al dar clic en
// "Ingresar" (referencia: admision.senati.edu.pe), en vez de un modal centrado — la URL se
// queda en "/" igual que antes. El fondo oscuro a la izquierda cierra al hacer clic (mismo
// patrón de botón-overlay que ya usa el menú móvil de Layout.tsx). Sin barra de cabecera: solo
// una X flotante arriba a la derecha, para no perder la forma de cerrar sin pasar por el
// fondo. El contenido se centra verticalmente dentro del panel (en vez de quedar pegado
// arriba con espacio vacío debajo). `visible` arranca en `false` y pasa a `true` un frame
// después de montar (requestAnimationFrame), para que el navegador pinte primero la posición
// de partida (`translate-x-full`, fuera de pantalla) antes de animar hacia `translate-x-0`.
export default function VerificacionModal({ onClose }: Props) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const id = requestAnimationFrame(() => setVisible(true))
    return () => cancelAnimationFrame(id)
  }, [])

  return (
    <div className="fixed inset-0 z-50 flex">
      <button type="button" aria-label="Cerrar" onClick={onClose} className="flex-1 bg-black/40" />
      <div
        className={`relative flex h-full w-full max-w-2xl flex-col overflow-hidden bg-white shadow-lg transition-transform duration-300 ${
          visible ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <button
          type="button"
          onClick={onClose}
          aria-label="Cerrar"
          className="absolute top-4 right-4 text-muted hover:text-ink"
        >
          <X size={22} />
        </button>
        <div className="flex flex-1 items-center justify-center overflow-y-auto p-6">
          <div className="w-full">
            <VerificacionPanel />
          </div>
        </div>
      </div>
    </div>
  )
}
