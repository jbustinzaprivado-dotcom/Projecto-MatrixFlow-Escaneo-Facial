import {
  BarChart3,
  Boxes,
  Building2,
  Combine,
  Grid3x3,
  History,
  ScanFace,
  ShieldCheck,
  ShoppingCart,
  SlidersHorizontal,
  Warehouse,
} from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import AccentCard, { ACCENT_BORDER } from '../../components/AccentCard'
import VerificacionModal from '../../components/VerificacionModal'
import { useAuth } from '../../context/AuthContext'
import type { AccentColor } from '../../components/AccentCard'

const MODULOS = [
  { icon: Building2, titulo: 'Empresa y sucursales', texto: 'Información corporativa, sedes y datos operativos.' },
  { icon: Boxes, titulo: 'Productos', texto: 'Catálogo, categorías y variables de análisis.' },
  { icon: ShoppingCart, titulo: 'Ventas', texto: 'Registro y análisis de cantidades e importes.' },
  { icon: Warehouse, titulo: 'Inventario', texto: 'Existencias y movimientos por sucursal.' },
  { icon: SlidersHorizontal, titulo: 'Vectores y matrices', texto: 'Información empresarial representada matemáticamente.' },
  { icon: Combine, titulo: 'Operaciones', texto: 'Suma, resta, producto escalar, combinación lineal y más.' },
  { icon: History, titulo: 'Historial', texto: 'Trazabilidad completa de cada cálculo ejecutado.' },
  { icon: BarChart3, titulo: 'Reportes', texto: 'Indicadores y gráficos de ventas por sucursal y producto.' },
]

// [Añadido] Las 6 franjas de color ya usadas en Dashboard/Auditoría, cicladas por posición
// sobre los 8 módulos — no hay una asignación semántica módulo→color obvia, así que ciclar
// es la opción más simple y neutral (las 2 últimas repiten primary/accent).
const ACCENTS = Object.keys(ACCENT_BORDER) as AccentColor[]

// [Añadido, "Fase B", D43] Portada pública — no existía ninguna antes de esta fase; "/"
// redirigía directo al login o al dashboard.
export default function Landing() {
  const { usuario } = useAuth()
  const [modalAbierto, setModalAbierto] = useState(false)

  return (
    <div className="min-h-screen bg-canvas">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <span className="text-lg font-semibold text-ink">MatrixFlow</span>
          {usuario ? (
            <Link to="/dashboard" className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white">
              Ir al Dashboard
            </Link>
          ) : (
            <button
              type="button"
              onClick={() => setModalAbierto(true)}
              className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
            >
              Ingresar
            </button>
          )}
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-6 py-20 text-center">
        <h1 className="text-4xl font-bold text-ink sm:text-5xl">MatrixFlow</h1>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-muted">
          Sistema web empresarial de análisis de ventas, inventario e indicadores — donde el
          álgebra lineal no es un módulo aparte, sino el mecanismo que convierte los datos de
          la empresa en resultados analíticos.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          {usuario ? (
            <Link
              to="/dashboard"
              className="flex items-center gap-2 rounded-md bg-primary px-6 py-3 text-sm font-semibold text-white"
            >
              <ScanFace size={18} />
              Ir al Dashboard
            </Link>
          ) : (
            <button
              type="button"
              onClick={() => setModalAbierto(true)}
              className="flex items-center gap-2 rounded-md bg-primary px-6 py-3 text-sm font-semibold text-white"
            >
              <ScanFace size={18} />
              Ingresar con DNI y rostro
            </button>
          )}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-20">
        <h2 className="mb-8 text-center text-2xl font-semibold text-ink">Módulos principales</h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {MODULOS.map(({ icon: Icon, titulo, texto }, i) => (
            <AccentCard key={titulo} accent={ACCENTS[i % ACCENTS.length]}>
              <Icon className="text-primary" size={28} />
              <h3 className="mt-4 font-semibold text-ink">{titulo}</h3>
              <p className="mt-2 text-sm text-muted">{texto}</p>
            </AccentCard>
          ))}
        </div>
      </section>

      <section className="bg-sidebar py-20 text-white">
        <div className="mx-auto grid max-w-6xl grid-cols-1 gap-10 px-6 sm:grid-cols-2">
          <div>
            <Grid3x3 className="text-accent" size={32} />
            <h2 className="mt-4 text-xl font-semibold">Núcleo matemático real</h2>
            <p className="mt-3 text-sm text-slate-300">
              Cada indicador nace de una operación de álgebra lineal calculada con Python y
              NumPy: cantidades × precios = ingresos, ventas reales − metas, combinaciones
              lineales ponderadas. Nada se simula — el motor matemático ejecuta y guarda cada
              resultado con su historial completo.
            </p>
          </div>
          <div>
            <ShieldCheck className="text-accent" size={32} />
            <h2 className="mt-4 text-xl font-semibold">Ingreso por DNI y verificación facial</h2>
            <p className="mt-3 text-sm text-slate-300">
              El acceso al sistema no usa usuario ni contraseña: se ingresa con el DNI y una
              verificación facial 1:1 real (detección y reconocimiento con OpenCV), que además
              entrega la sesión y el rol de quien ingresa.
            </p>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-200 py-6 text-center text-sm text-muted">
        MatrixFlow
      </footer>

      {modalAbierto && <VerificacionModal onClose={() => setModalAbierto(false)} />}
    </div>
  )
}
