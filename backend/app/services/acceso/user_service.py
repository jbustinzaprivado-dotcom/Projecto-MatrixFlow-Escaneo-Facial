from sqlalchemy.orm import Session

from app.core.errors import ApiException
from app.repositories.empresa import branch_repository
from app.repositories.acceso import role_repository, user_repository
from app.schemas.acceso.user_schema import CarnetOut, UsuarioCreate, UsuarioOut


def _to_out(usuario) -> UsuarioOut:
    return UsuarioOut(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        dni=usuario.dni,
        rol=usuario.rol.nombre,
        sucursal_id=usuario.sucursal_id,
        activo=usuario.activo,
        creado_en=usuario.creado_en,
        rostros=len(usuario.rostros),
    )


def list_usuarios(db: Session) -> list[UsuarioOut]:
    return [_to_out(u) for u in user_repository.list_all(db)]


def create_usuario(db: Session, data: UsuarioCreate) -> UsuarioOut:
    if user_repository.get_by_dni(db, data.dni) is not None:
        raise ApiException(409, "Ya existe un usuario con ese DNI.")
    if user_repository.get_by_email(db, data.email) is not None:
        raise ApiException(409, "Ya existe un usuario con ese correo.")
    rol = role_repository.get_by_nombre(db, data.rol)
    if rol is None:
        raise ApiException(500, f"El rol «{data.rol}» no existe en la base de datos.")
    sucursal = branch_repository.get(db, data.sucursal_id)
    if sucursal is None:
        raise ApiException(404, "La sucursal no existe.")

    usuario = user_repository.create(
        db, nombre=data.nombre, email=data.email, dni=data.dni, rol_id=rol.id, sucursal_id=sucursal.id
    )
    return _to_out(usuario)


def get_carnet(db: Session, usuario_id: int) -> CarnetOut:
    usuario = user_repository.get(db, usuario_id)
    if usuario is None:
        raise ApiException(404, "El usuario no existe.")
    return CarnetOut(
        nombre=usuario.nombre,
        dni=usuario.dni,
        rol=usuario.rol.nombre,
        sede=usuario.sucursal.nombre if usuario.sucursal else "—",
        activo=usuario.activo,
        creado_en=usuario.creado_en,
    )
