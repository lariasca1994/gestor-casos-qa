"""Gestion de cuentas de usuario: listar, suspender, reactivar y eliminar.

Todo este router es exclusivo de ADMIN (Depends(exigir_admin) en cada ruta).
Un ADMIN no puede suspenderse ni eliminarse a si mismo por accidente: eso
rompería su propia sesion sin que se de cuenta, asi que esas dos rutas
verifican que el usuario_id de la URL no sea el del ADMIN que hace el
pedido."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import NoAutorizado, exigir_admin
from app.repositorios import usuarios as repo_usuarios

router = APIRouter(prefix="/admin/usuarios")
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def listar(request: Request, usuario: dict = Depends(exigir_admin)):
    return templates.TemplateResponse(
        "admin/usuarios.html",
        {
            "request": request,
            "usuario": usuario,
            "usuarios": repo_usuarios.listar_todos(),
        },
    )


@router.post("/{usuario_id}/suspender")
def suspender(usuario_id: str, usuario: dict = Depends(exigir_admin)):
    if usuario_id == str(usuario["_id"]):
        raise NoAutorizado()
    repo_usuarios.suspender(usuario_id)
    return RedirectResponse(url="/admin/usuarios", status_code=303)


@router.post("/{usuario_id}/reactivar")
def reactivar(usuario_id: str, usuario: dict = Depends(exigir_admin)):
    repo_usuarios.reactivar(usuario_id)
    return RedirectResponse(url="/admin/usuarios", status_code=303)


@router.post("/{usuario_id}/eliminar")
def eliminar(usuario_id: str, usuario: dict = Depends(exigir_admin)):
    if usuario_id == str(usuario["_id"]):
        raise NoAutorizado()
    repo_usuarios.eliminar(usuario_id)
    return RedirectResponse(url="/admin/usuarios", status_code=303)
