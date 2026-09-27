// Sesión real [Añadido, Fase 6 — corrige D44]: el token lo emite `POST /verificacion` al
// coincidir (D70), no un login de usuario/contraseña (D17). Se centraliza aquí la lectura y
// escritura en localStorage para que http.ts (interceptor) y AuthContext (estado de React)
// lean exactamente el mismo formato.
import type { Rol } from '../types/domain'

const STORAGE_KEY = 'matrixflow_sesion'

export interface SesionUsuario {
  nombre: string
  dni: string
  rol: Rol
}

export interface SesionAlmacenada {
  token: string
  usuario: SesionUsuario
}

export function leerSesion(): SesionAlmacenada | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as SesionAlmacenada) : null
  } catch {
    return null
  }
}

export function guardarSesion(sesion: SesionAlmacenada): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sesion))
}

export function borrarSesion(): void {
  localStorage.removeItem(STORAGE_KEY)
}
