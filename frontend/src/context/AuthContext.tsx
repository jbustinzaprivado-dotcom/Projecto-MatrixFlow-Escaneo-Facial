import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { borrarSesion, guardarSesion, leerSesion, type SesionUsuario } from '../services/session'

interface AuthContextValue {
  token: string | null
  usuario: SesionUsuario | null
  login: (token: string, usuario: SesionUsuario) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

// [Añadido, Fase 6 — corrige D44] Estado de sesión real en toda la app: lo abre `POST
// /verificacion` al coincidir (D70), lo cierra el propio usuario o un 401 del backend
// (token inválido o expirado — ver el interceptor de http.ts).
export function AuthProvider({ children }: { children: ReactNode }) {
  const [sesion, setSesion] = useState(() => leerSesion())

  useEffect(() => {
    function cerrarPorEventoExterno() {
      setSesion(null)
    }
    window.addEventListener('matrixflow:sesion-cerrada', cerrarPorEventoExterno)
    return () => window.removeEventListener('matrixflow:sesion-cerrada', cerrarPorEventoExterno)
  }, [])

  function login(token: string, usuario: SesionUsuario) {
    guardarSesion({ token, usuario })
    setSesion({ token, usuario })
  }

  function logout() {
    borrarSesion()
    setSesion(null)
  }

  return (
    <AuthContext.Provider
      value={{ token: sesion?.token ?? null, usuario: sesion?.usuario ?? null, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth debe usarse dentro de <AuthProvider>')
  return ctx
}
