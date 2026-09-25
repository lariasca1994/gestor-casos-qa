"""Identificacion del usuario a partir de la cookie de sesion, y control de
acceso: cada proyecto solo lo puede ver/editar su dueno o un ADMIN."""

from fastapi import Depends, Request

from app.config import COOKIE_SESION, ROL_ADMIN
from app.repositorios.usuarios import buscar_por_id
from app.seguridad import leer_token


class RequiereLogin(Exception):
    """No hay sesion valida: la pagina protegida no se puede mostrar."""


class NoAutorizado(Exception):
    """Hay sesion, pero el rol del usuario no alcanza para esta accion."""


def usuario_actual(request: Request) -> dict | None:
    """Devuelve el usuario de la sesion activa, o None si no hay ninguna.

    El usuario se relee de Mongo por _id en cada request (no solo del JWT),
    asi que una cuenta que un ADMIN acaba de suspender queda deslogueada de
    inmediato, sin esperar a que expire el token."""
    token = request.cookies.get(COOKIE_SESION)
    if not token:
        return None
    carga = leer_token(token)
    if not carga:
        return None
    usuario = buscar_por_id(carga["sub"])
    if usuario is None or not usuario.get("activo", True):
        return None
    return usuario


def exigir_login(request: Request) -> dict:
    """Para usar con Depends(): devuelve el usuario o lanza RequiereLogin."""
    usuario = usuario_actual(request)
    if not usuario:
        raise RequiereLogin()
    return usuario


def exigir_admin(request: Request) -> dict:
    usuario = exigir_login(request)
    if usuario.get("rol") != ROL_ADMIN:
        raise NoAutorizado()
    return usuario


def es_admin(usuario: dict) -> bool:
    return usuario.get("rol") == ROL_ADMIN


def proyecto_autorizado(proyecto_id: str, usuario: dict = Depends(exigir_login)) -> dict:
    """Para usar con Depends() en cualquier ruta que tenga {proyecto_id}:
    exige sesion y que el usuario sea ADMIN o el dueno del proyecto. Los
    usuarios QA solo ven su propio proyecto; el ADMIN ve todos. Devuelve el
    proyecto ya cargado para que el router no tenga que volver a pedirlo."""
    # import local para evitar import circular (proyectos no depende de este modulo)
    from app.repositorios.proyectos import obtener as obtener_proyecto

    proyecto = obtener_proyecto(proyecto_id)
    if proyecto is None:
        raise NoAutorizado()
    if not es_admin(usuario) and proyecto.get("creado_por") != str(usuario["_id"]):
        raise NoAutorizado()
    return proyecto
