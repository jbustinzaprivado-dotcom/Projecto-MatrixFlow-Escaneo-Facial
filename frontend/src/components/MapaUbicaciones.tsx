import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png'
import icon from 'leaflet/dist/images/marker-icon.png'
import shadow from 'leaflet/dist/images/marker-shadow.png'
import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet'
import type { UbicacionActiva } from '../types/domain'

// [Añadido, corrige D9, D134] Vite no resuelve las rutas relativas que Leaflet arma por
// defecto para su ícono (problema conocido de la comunidad, no un bug de este proyecto). Se
// reemplaza una sola vez al cargar este módulo, con las 3 imágenes importadas explícitamente
// desde el propio paquete.
delete (L.Icon.Default.prototype as { _getIconUrl?: unknown })._getIconUrl
L.Icon.Default.mergeOptions({ iconRetinaUrl: iconRetina, iconUrl: icon, shadowUrl: shadow })

// Centro de Perú, solo como fallback cuando no hay nadie activo todavía.
const CENTRO_PERU: [number, number] = [-9.19, -75.015]

export default function MapaUbicaciones({ ubicaciones }: { ubicaciones: UbicacionActiva[] }) {
  const centro: [number, number] =
    ubicaciones.length > 0
      ? [
          ubicaciones.reduce((s, u) => s + u.latitud, 0) / ubicaciones.length,
          ubicaciones.reduce((s, u) => s + u.longitud, 0) / ubicaciones.length,
        ]
      : CENTRO_PERU

  return (
    <MapContainer
      center={centro}
      zoom={ubicaciones.length > 0 ? 12 : 5}
      style={{ height: 320, width: '100%' }}
      className="rounded-md"
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      />
      {ubicaciones.map((u) => (
        <Marker key={u.usuarioId} position={[u.latitud, u.longitud]}>
          <Popup>
            <strong>{u.usuario}</strong> ({u.rol})
            <br />
            {u.sede}
            <br />
            Actualizado: {new Date(u.actualizadoEn).toLocaleTimeString('es-PE')}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
