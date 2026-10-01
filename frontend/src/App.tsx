import { Suspense, lazy } from 'react'
import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import { useAuth } from './context/AuthContext'

// Cada página se carga bajo demanda [Añadido, misma práctica de rendimiento del proyecto de
// referencia], para no bajar todo el bundle de una sola vez.
const Landing = lazy(() => import('./pages/publico/Landing'))
const Ingresar = lazy(() => import('./pages/publico/Ingresar'))
const Dashboard = lazy(() => import('./pages/reportes/Dashboard'))
const Empresa = lazy(() => import('./pages/empresa/Empresa'))
const Sucursales = lazy(() => import('./pages/empresa/Sucursales'))
const Productos = lazy(() => import('./pages/empresa/Productos'))
const Ventas = lazy(() => import('./pages/operacion/Ventas'))
const Inventario = lazy(() => import('./pages/operacion/Inventario'))
const Vectores = lazy(() => import('./pages/algebra/Vectores'))
const Matrices = lazy(() => import('./pages/algebra/Matrices'))
const Operaciones = lazy(() => import('./pages/algebra/Operaciones'))
const Combinaciones = lazy(() => import('./pages/algebra/Combinaciones'))
const Historial = lazy(() => import('./pages/algebra/Historial'))
const Reportes = lazy(() => import('./pages/reportes/Reportes'))
const Auditoria = lazy(() => import('./pages/acceso/Auditoria'))
const Usuarios = lazy(() => import('./pages/acceso/Usuarios'))
const Carnet = lazy(() => import('./pages/acceso/Carnet'))
const Configuracion = lazy(() => import('./pages/empresa/Configuracion'))

// [Añadido, Fase 6 — corrige D24] Sin sesión (D70), redirige a /ingresar en vez de mostrar
// el módulo. Antes de esta fase cualquiera podía escribir la URL directa sin pasar por el
// login biométrico.
function RutaProtegida() {
  const { token } = useAuth()
  if (!token) return <Navigate to="/ingresar" replace />
  return <Outlet />
}

export default function App() {
  return (
    <Suspense fallback={<div className="p-8 text-sm text-muted">Cargando…</div>}>
      <Routes>
        {/* [Añadido, "Fase B", D43] Portada pública; antes "/" redirigía directo al login */}
        <Route path="/" element={<Landing />} />
        {/* [Añadido D5, D6] reemplaza el /login genérico de [PDF §8.3] por DNI + rostro */}
        <Route path="/ingresar" element={<Ingresar />} />

        <Route element={<RutaProtegida />}>
          <Route element={<Layout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/empresa" element={<Empresa />} />
            <Route path="/sucursales" element={<Sucursales />} />
            <Route path="/productos" element={<Productos />} />
            <Route path="/ventas" element={<Ventas />} />
            <Route path="/inventario" element={<Inventario />} />
            <Route path="/vectores" element={<Vectores />} />
            <Route path="/matrices" element={<Matrices />} />
            <Route path="/operaciones" element={<Operaciones />} />
            <Route path="/combinaciones" element={<Combinaciones />} />
            <Route path="/historial" element={<Historial />} />
            <Route path="/reportes" element={<Reportes />} />
            <Route path="/auditoria" element={<Auditoria />} />
            <Route path="/usuarios" element={<Usuarios />} />
            <Route path="/usuarios/:id/carnet" element={<Carnet />} />
            <Route path="/configuracion" element={<Configuracion />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Route>
      </Routes>
    </Suspense>
  )
}
