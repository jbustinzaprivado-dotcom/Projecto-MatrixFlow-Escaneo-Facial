import {
  Boxes,
  Building2,
  ClipboardList,
  Combine,
  Grid3x3,
  History,
  Home,
  LogOut,
  type LucideIcon,
  Menu,
  Settings,
  ShieldCheck,
  ShoppingCart,
  SlidersHorizontal,
  Users,
  Warehouse,
  X,
} from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useUbicacionHeartbeat } from '../hooks/useUbicacionHeartbeat'

const ROL_LABEL = { administrador: 'Administrador', analista: 'Analista', consulta: 'Consulta' }

interface NavItem {
  to: string
  label: string
  icon: LucideIcon
  indent?: boolean
  group?: string
}

// Navegación [PDF §8.2], más "Auditoría" [Añadido D5] junto a Usuarios/Configuración
const NAV: NavItem[] = [
  { to: '/dashboard', label: 'Dashboard', icon: Home },
  { to: '/empresa', label: 'Empresa', icon: Building2 },
  { to: '/sucursales', label: 'Sucursales', icon: Building2, indent: true },
  { to: '/productos', label: 'Productos', icon: Boxes, indent: true },
  { to: '/ventas', label: 'Ventas', icon: ShoppingCart },
  { to: '/inventario', label: 'Inventario', icon: Warehouse },
  { to: '/vectores', label: 'Vectores', icon: SlidersHorizontal, group: 'Análisis Matemático' },
  { to: '/matrices', label: 'Matrices', icon: Grid3x3, indent: true },
  { to: '/operaciones', label: 'Operaciones', icon: Combine, indent: true },
  { to: '/combinaciones', label: 'Combinaciones lineales', icon: Combine, indent: true },
  { to: '/historial', label: 'Historial', icon: History },
  { to: '/reportes', label: 'Reportes', icon: ClipboardList },
  { to: '/auditoria', label: 'Auditoría', icon: ShieldCheck },
  { to: '/usuarios', label: 'Usuarios', icon: Users },
  { to: '/configuracion', label: 'Configuración', icon: Settings },
]

function SidebarContent() {
  const { usuario, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <nav className="flex h-full flex-col gap-1 p-4">
      <div className="mb-4 px-2 text-lg font-semibold text-white">MatrixFlow</div>
      {NAV.map(({ to, label, icon: Icon, indent, group }) => (
        <div key={to}>
          {group && (
            <div className="mt-3 mb-1 px-2 text-xs font-semibold tracking-wide text-slate-400 uppercase">
              {group}
            </div>
          )}
          <NavLink
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-2 rounded-full px-3 py-2 text-sm transition-colors ${
                indent ? 'ml-3' : ''
              } ${
                isActive
                  ? 'bg-primary text-white'
                  : 'text-slate-300 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        </div>
      ))}

      {/* [Añadido, Fase 6 — corrige D44] Sesión real abierta por el login biométrico (D70) */}
      {usuario && (
        <div className="mt-auto border-t border-white/10 pt-3">
          <div className="px-2 text-sm font-medium text-white">{usuario.nombre}</div>
          <div className="px-2 text-xs text-slate-400">{ROL_LABEL[usuario.rol]}</div>
          <button
            type="button"
            onClick={() => {
              logout()
              navigate('/ingresar', { replace: true })
            }}
            className="mt-2 flex w-full items-center gap-2 rounded-full px-3 py-2 text-sm text-slate-300 hover:bg-white/5 hover:text-white"
          >
            <LogOut size={16} /> Cerrar sesión
          </button>
        </div>
      )}
    </nav>
  )
}

export default function Layout() {
  useUbicacionHeartbeat()
  const [open, setOpen] = useState(false)

  return (
    // [Añadido, feedback del equipo] Antes era `min-h-screen` con scroll de toda la página:
    // el `<aside>` mide exactamente 100vh, así que al bajar en una tabla larga (Inventario)
    // el fondo del sidebar se acababa a mitad de pantalla. Ahora el layout mide 100vh fijo y
    // solo `<main>` scrollea verticalmente — el sidebar siempre llena la pantalla, y nunca se
    // agrega scroll horizontal.
    <div className="flex h-screen overflow-hidden">
      <a
        href="#contenido"
        className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:m-2 focus:rounded focus:bg-primary focus:px-3 focus:py-2 focus:text-white"
      >
        Saltar al contenido
      </a>

      <aside className="hidden h-screen w-64 shrink-0 overflow-y-auto bg-sidebar md:block">
        <SidebarContent />
      </aside>

      {open && (
        <div className="fixed inset-0 z-40 md:hidden">
          <button
            type="button"
            aria-label="Cerrar menú"
            className="absolute inset-0 bg-black/40"
            onClick={() => setOpen(false)}
          />
          <div className="relative z-50 h-full w-64 bg-sidebar">
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="absolute top-3 right-3 text-slate-300"
              aria-label="Cerrar menú"
            >
              <X size={20} />
            </button>
            <SidebarContent />
          </div>
        </div>
      )}

      <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="flex items-center gap-3 border-b border-slate-200 bg-white px-4 py-3 md:hidden">
          <button
            type="button"
            onClick={() => setOpen(true)}
            aria-label="Abrir menú"
            className="text-ink"
          >
            <Menu size={22} />
          </button>
          <span className="font-semibold">MatrixFlow</span>
        </header>

        <main id="contenido" className="flex-1 overflow-y-auto p-4 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
