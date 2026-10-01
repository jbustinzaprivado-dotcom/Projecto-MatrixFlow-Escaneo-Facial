// Capa de servicio consumida por las páginas. Desde la Fase 7 (Analítica, [PDF §14]) ya no
// queda ningún dato simulado: todo llama al backend real.
import { http } from './http'
import type {
  AuditoriaEntry,
  Empresa,
  InventarioItem,
  MatrizRegistro,
  OperacionHistorial,
  Producto,
  ReporteVentas,
  Rol,
  Sede,
  TipoOperacion,
  UbicacionActiva,
  Usuario,
  VectorRegistro,
  Venta,
  VerificacionResultado,
} from '../types/domain'

// ---------------------------------------------------------------------------
// Empresa, sucursales, productos [PDF §9.2] — sin mapeo: los nombres de campo ya coinciden.
// ---------------------------------------------------------------------------

interface EmpresaApi {
  id: number
  razon_social: string
  ruc: string
  rubro: string
}

export async function getEmpresa(): Promise<Empresa> {
  const { data } = await http.get<EmpresaApi>('/companies')
  return { id: data.id, razonSocial: data.razon_social, ruc: data.ruc, rubro: data.rubro }
}

export async function getSedes(): Promise<Sede[]> {
  const { data } = await http.get<Sede[]>('/branches')
  return data
}

export async function getProductos(): Promise<Producto[]> {
  const { data } = await http.get<Producto[]>('/products')
  return data
}

// ---------------------------------------------------------------------------
// Usuarios y login biométrico [Añadido, Fase A / Fase A2]
// ---------------------------------------------------------------------------

interface UsuarioApi {
  id: number
  nombre: string
  email: string
  dni: string
  rol: Rol
  sucursal_id: number | null
  activo: boolean
  creado_en: string
  rostros: number
}

function mapUsuario(u: UsuarioApi): Usuario {
  return {
    id: u.id,
    nombre: u.nombre,
    email: u.email,
    dni: u.dni,
    rol: u.rol,
    activo: u.activo,
    sedeId: u.sucursal_id ?? 0,
    creadoEn: u.creado_en,
  }
}

export async function getUsuarios(): Promise<Usuario[]> {
  const { data } = await http.get<UsuarioApi[]>('/users')
  return data.map(mapUsuario)
}

export interface NuevoUsuarioInput {
  nombre: string
  email: string
  dni: string
  rol: Rol
  sedeId: number
}

export async function crearUsuario(input: NuevoUsuarioInput): Promise<Usuario> {
  const { data } = await http.post<UsuarioApi>('/users', {
    nombre: input.nombre,
    email: input.email,
    dni: input.dni,
    rol: input.rol,
    sucursal_id: input.sedeId,
  })
  return mapUsuario(data)
}

/** [Añadido, Fase A] Sube una foto y la convierte en el vector guardado del usuario. */
export async function registrarRostro(usuarioId: number, imagen: Blob) {
  const formulario = new FormData()
  formulario.append('imagen', imagen, 'rostro.jpg')
  const { data } = await http.post<{ usuario_id: number; imagenes_guardadas: number }>(
    `/users/${usuarioId}/rostro`,
    formulario,
  )
  return { usuarioId: data.usuario_id, imagenesGuardadas: data.imagenes_guardadas }
}

interface VerificacionApi {
  coincide: boolean
  similitud: number
  usuario?: {
    nombre: string
    dni: string
    rol: Rol
    sede: string
    activo: boolean
    creado_en: string
  } | null
  token?: string | null
}

/** [Añadido D6] Verificación 1:1 real contra el motor facial (SFace). Envía el DNI y la
 * foto capturada; el backend compara solo contra los vectores de ese usuario. */
export async function verificarPorDni(dni: string, imagen: Blob): Promise<VerificacionResultado> {
  const formulario = new FormData()
  formulario.append('dni', dni)
  formulario.append('imagen', imagen, 'rostro.jpg')
  const { data } = await http.post<VerificacionApi>('/verificacion', formulario)
  return {
    coincide: data.coincide,
    similitud: data.similitud,
    usuario: data.usuario
      ? {
          nombre: data.usuario.nombre,
          dni: data.usuario.dni,
          rol: data.usuario.rol,
          sede: data.usuario.sede,
          activo: data.usuario.activo,
          creadoEn: data.usuario.creado_en,
        }
      : undefined,
    token: data.token ?? undefined,
  }
}

interface CarnetApi {
  nombre: string
  dni: string
  rol: Rol
  sede: string
  activo: boolean
  creado_en: string
}

/** [Añadido D8] datos del carnet: nombre, DNI, rol, sede y hora de registro. Nunca una foto. */
export async function getCarnet(usuarioId: number) {
  try {
    const { data } = await http.get<CarnetApi>(`/users/${usuarioId}/carnet`)
    return data
  } catch {
    return null
  }
}

// ---------------------------------------------------------------------------
// Ventas e inventario [PDF §9.2] — mapeo snake_case -> camelCase.
// ---------------------------------------------------------------------------

interface VentaApi {
  id: number
  sucursal_id: number
  producto_id: number
  cantidad: number
  importe: number
  fecha: string
}

export async function getVentas(): Promise<Venta[]> {
  const { data } = await http.get<VentaApi[]>('/sales')
  return data.map((v) => ({
    id: v.id,
    sedeId: v.sucursal_id,
    productoId: v.producto_id,
    cantidad: v.cantidad,
    importe: v.importe,
    fecha: v.fecha,
  }))
}

interface InventarioApi {
  id: number
  sucursal_id: number
  producto_id: number
  existencias: number
  actualizado_en: string
}

export async function getInventario(): Promise<InventarioItem[]> {
  const { data } = await http.get<InventarioApi[]>('/inventory')
  return data.map((i) => ({
    id: i.id,
    sedeId: i.sucursal_id,
    productoId: i.producto_id,
    existencias: i.existencias,
    actualizadoEn: i.actualizado_en,
  }))
}

/** [RF-06, Añadido en el repaso de fidelidad §16-21] Registra una entrada o salida real. */
export async function registrarMovimiento(input: {
  sedeId: number
  productoId: number
  tipo: 'entrada' | 'salida'
  cantidad: number
}): Promise<void> {
  await http.post('/inventory/movimientos', {
    sucursal_id: input.sedeId,
    producto_id: input.productoId,
    tipo: input.tipo,
    cantidad: input.cantidad,
  })
}

// ---------------------------------------------------------------------------
// Vectores y matrices [PDF §9.2, §11]
// ---------------------------------------------------------------------------

interface VectorApi {
  id: number
  nombre: string
  valores: number[]
  origen: string
  creado_en: string
}

export async function getVectores(): Promise<VectorRegistro[]> {
  const { data } = await http.get<VectorApi[]>('/vectors')
  return data.map((v) => ({ id: v.id, nombre: v.nombre, valores: v.valores, origen: v.origen, creadoEn: v.creado_en }))
}

interface MatrizApi {
  id: number
  nombre: string
  valores: number[][]
  origen: string
  creado_en: string
}

export async function getMatrices(): Promise<MatrizRegistro[]> {
  const { data } = await http.get<MatrizApi[]>('/matrices')
  return data.map((m) => ({
    id: m.id,
    nombre: m.nombre,
    valores: m.valores,
    filas: m.valores.length,
    columnas: m.valores[0]?.length ?? 0,
    origen: m.origen,
    creadoEn: m.creado_en,
  }))
}

// ---------------------------------------------------------------------------
// Operaciones e historial [PDF §9.2, §11] — corrige D22: el cálculo ya no se
// hace en el navegador, lo hace el backend con NumPy (Fase 4).
// ---------------------------------------------------------------------------

export interface OperacionCreateInput {
  tipo: TipoOperacion
  vectorAId?: number
  vectorBId?: number
  matrizAId?: number
  matrizBId?: number
  escalar?: number
  coeficienteA?: number
  coeficienteB?: number
}

interface OperacionApi {
  id: number
  tipo: TipoOperacion
  entradas: string
  resultado: string | null
  estado: 'pendiente' | 'ok' | 'error'
  mensaje: string
  creado_en: string
}

function mapOperacion(o: OperacionApi): OperacionHistorial {
  return {
    id: o.id,
    tipo: o.tipo,
    entradas: o.entradas,
    resultado: o.resultado ?? o.mensaje,
    usuario: '—', // sin sesión todavía (D44): ninguna operación tiene un usuario que la firme
    fecha: o.creado_en,
    estado: o.estado,
  }
}

export async function crearOperacion(input: OperacionCreateInput): Promise<OperacionHistorial> {
  const { data } = await http.post<OperacionApi>('/operations', {
    tipo: input.tipo,
    vector_a_id: input.vectorAId,
    vector_b_id: input.vectorBId,
    matriz_a_id: input.matrizAId,
    matriz_b_id: input.matrizBId,
    escalar: input.escalar,
    coeficiente_a: input.coeficienteA,
    coeficiente_b: input.coeficienteB,
  })
  return mapOperacion(data)
}

export async function getHistorial(): Promise<OperacionHistorial[]> {
  const { data } = await http.get<OperacionApi[]>('/operations')
  return data.map(mapOperacion)
}

// ---------------------------------------------------------------------------
// Reportes [PDF §9.2] — el backend ya agrega con SQL; el navegador ya no calcula nada.
// ---------------------------------------------------------------------------

interface ReporteApi {
  ventas_por_sucursal: { sucursal: string; importe: number }[]
  ventas_por_producto: { producto: string; cantidad: number }[]
}

export async function getReportes(): Promise<ReporteVentas> {
  const { data } = await http.get<ReporteApi>('/reports')
  return { ventasPorSucursal: data.ventas_por_sucursal, ventasPorProducto: data.ventas_por_producto }
}

// ---------------------------------------------------------------------------
// Dashboard [PDF §14] — real desde la Fase 7 (corrige D62): el backend agrega con SQL,
// igual que ya hacía /reports desde la Fase 5.
// ---------------------------------------------------------------------------

interface DashboardResumenApi {
  total_sedes: number
  total_productos: number
  total_ventas: number
  total_unidades: number
  operaciones_ejecutadas: number
  tendencia_semanal: { semana: string; total: number }[]
  ventas_por_sede: { sede: string; total: number }[]
}

export async function getDashboardResumen() {
  const { data } = await http.get<DashboardResumenApi>('/dashboard')
  return {
    totalSedes: data.total_sedes,
    totalProductos: data.total_productos,
    totalVentas: data.total_ventas,
    totalUnidades: data.total_unidades,
    operacionesEjecutadas: data.operaciones_ejecutadas,
    tendenciaSemanal: data.tendencia_semanal,
    ventasPorSede: data.ventas_por_sede,
  }
}

// ---------------------------------------------------------------------------
// Auditoría [Añadido D5, D9] — real desde la Fase 6 (D73): lee `audit_logs` [PDF §10],
// que cada intento de verificación (D70) ya escribe. Corrige D63 (dependía de sesión real).
// ---------------------------------------------------------------------------

interface AuditoriaResumenApi {
  actividad_por_dia: { dia: string; cantidad: number }[]
  mas_activos: { usuario: string; cantidad: number }[]
  total_7_dias: number
}

export async function getAuditoria() {
  const { data } = await http.get<AuditoriaEntry[]>('/audit')
  return data
}

export async function getAuditoriaResumen() {
  const { data } = await http.get<AuditoriaResumenApi>('/audit/resumen')
  return {
    actividadPorDia: data.actividad_por_dia,
    masActivos: data.mas_activos,
    total7Dias: data.total_7_dias,
  }
}

// ---------------------------------------------------------------------------
// Ubicación en vivo [Añadido, corrige D9] — heartbeat cada 60s (Layout.tsx) + mapa en
// Auditoría, solo administrador.
// ---------------------------------------------------------------------------

export async function reportarUbicacion(input: {
  latitud: number
  longitud: number
  precisionM?: number
}): Promise<void> {
  await http.post('/ubicacion', {
    latitud: input.latitud,
    longitud: input.longitud,
    precision_m: input.precisionM,
  })
}

interface UbicacionActivaApi {
  usuario_id: number
  usuario: string
  rol: Rol
  sede: string
  latitud: number
  longitud: number
  precision_m: number | null
  actualizado_en: string
}

export async function getUbicacionesActivas(): Promise<UbicacionActiva[]> {
  const { data } = await http.get<UbicacionActivaApi[]>('/ubicacion/activas')
  return data.map((u) => ({
    usuarioId: u.usuario_id,
    usuario: u.usuario,
    rol: u.rol,
    sede: u.sede,
    latitud: u.latitud,
    longitud: u.longitud,
    precisionM: u.precision_m,
    actualizadoEn: u.actualizado_en,
  }))
}
