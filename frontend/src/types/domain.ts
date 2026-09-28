// Tipos de dominio de MatrixFlow [PDF §5, §10, §11]

export type Rol = 'administrador' | 'analista' | 'consulta'

export interface Usuario {
  id: number
  nombre: string
  email: string
  /** [Añadido D6] usado para el ingreso por DNI + verificación facial 1:1 */
  dni: string
  rol: Rol
  activo: boolean
  sedeId: number
  creadoEn: string
}

export interface Sede {
  id: number
  nombre: string
  /** [Añadido D9] ubicación fija configurada por un administrador, usada por la auditoría */
  departamento: string
  distrito: string
  direccion: string
}

export interface Producto {
  id: number
  nombre: string
  categoria: string
  precio: number
}

export interface Venta {
  id: number
  sedeId: number
  productoId: number
  cantidad: number
  importe: number
  fecha: string
}

export interface InventarioItem {
  id: number
  sedeId: number
  productoId: number
  existencias: number
  actualizadoEn: string
}

export interface VectorRegistro {
  id: number
  nombre: string
  valores: number[]
  origen: string
  creadoEn: string
}

export interface MatrizRegistro {
  id: number
  nombre: string
  filas: number
  columnas: number
  valores: number[][]
  origen: string
  creadoEn: string
}

export type TipoOperacion =
  | 'suma_vector'
  | 'resta_vector'
  | 'escalar_vector'
  | 'producto_escalar'
  | 'suma_matriz'
  | 'resta_matriz'
  | 'multiplicacion_matriz'
  | 'transpuesta_matriz'
  | 'escalar_matriz'
  | 'combinacion_lineal'

export interface OperacionHistorial {
  id: number
  tipo: TipoOperacion
  entradas: string
  resultado: string
  usuario: string
  fecha: string
  /** `pendiente` puede aparecer en filas antiguas, de antes de que existiera el motor NumPy real (Fase 4). */
  estado: 'ok' | 'error' | 'pendiente'
}

/** [PDF §10: tabla `companies`] */
export interface Empresa {
  id: number
  razonSocial: string
  ruc: string
  rubro: string
}

export interface ReporteVentas {
  ventasPorSucursal: { sucursal: string; importe: number }[]
  ventasPorProducto: { producto: string; cantidad: number }[]
}

/** [Añadido D5, D9] fila de auditoría extendida: quién, qué, cuándo y desde qué sede */
export interface AuditoriaEntry {
  id: number
  usuario: string
  accion: string
  recurso: string
  resultado: 'ok' | 'error'
  fecha: string
  sede: string
}

/** [Añadido D6, D7, D8] resultado de la verificación por DNI + rostro (1:1, sin candidato si no coincide).
 * Desde la Fase 6, `token` trae la sesión real cuando coincide (corrige D44). */
export interface VerificacionResultado {
  coincide: boolean
  usuario?: Pick<Usuario, 'nombre' | 'dni' | 'rol' | 'activo'> & { sede: string; creadoEn: string }
  similitud?: number
  token?: string
}
