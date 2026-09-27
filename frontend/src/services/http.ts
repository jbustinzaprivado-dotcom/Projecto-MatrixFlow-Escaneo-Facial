import axios from 'axios'
import { borrarSesion, leerSesion } from './session'

// Cliente HTTP real desde la Fase 5. Desde la Fase 6, cada petición agrega el JWT de la
// sesión (D70) y un 401 la cierra sola — sesión inválida o expirada, no queda otra opción
// que ingresar de nuevo por DNI + rostro.
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const http = axios.create({ baseURL: `${API_URL}/api/v1` })

http.interceptors.request.use((config) => {
  const sesion = leerSesion()
  if (sesion?.token) {
    config.headers.Authorization = `Bearer ${sesion.token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      borrarSesion()
      window.dispatchEvent(new Event('matrixflow:sesion-cerrada'))
    }
    return Promise.reject(error)
  },
)
