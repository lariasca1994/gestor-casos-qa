"""Paginas de Proyectos: listar, crear, editar y archivar (solo ADMIN).

Cada QA solo ve y edita sus propios proyectos; el ADMIN ve y edita todos."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import es_admin, exigir_admin, exigir_login, proyecto_autorizado
from app.repositorios import proyectos as repo_proyectos
from app.repositorios import usuarios as repo_usuarios

router = APIRouter(prefix="/proyectos")
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def listar(request: Request, usuario: dict = Depends(exigir_login)):
    admin = es_admin(usuario)
    filtro_creador = None if admin else str(usuario["_id"])
    proyectos = repo_proyectos.listar(creado_por=filtro_creador)
    if admin:
        # El ADMIN ve todos los proyectos: aclarar de quien es cada uno.
        for proyecto in proyectos:
            dueno = repo_usuarios.buscar_por_id(proyecto.get("creado_por", ""))
            proyecto["creado_por_nombre"] = dueno["nombre"] if dueno else "?"
    return templates.TemplateResponse(
        "proyectos/lista.html",
        {
            "request": request,
            "usuario": usuario,
            "proyectos": proyectos,
            "mostrar_dueno": admin,
        },
    )


@router.get("/nuevo", response_class=HTMLResponse)
def formulario_nuevo(request: Request, usuario: dict = Depends(exigir_login)):
    return templates.TemplateResponse(
        "proyectos/formulario.html",
        {"request": request, "usuario": usuario, "proyecto": None, "error": None},
    )


@router.post("/nuevo")
def crear(
    request: Request,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    usuario: dict = Depends(exigir_login),
):
    if not nombre.strip():
        return templates.TemplateResponse(
            "proyectos/formulario.html",
            {
                "request": request,
                "usuario": usuario,
                "proyecto": None,
                "error": "El nombre es obligatorio.",
            },
            status_code=400,
        )
    repo_proyectos.crear(nombre, descripcion, creado_por=str(usuario["_id"]))
    return RedirectResponse(url="/proyectos", status_code=303)


@router.get("/{proyecto_id}/editar", response_class=HTMLResponse)
def formulario_editar(
    request: Request,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "proyectos/formulario.html",
        {"request": request, "usuario": usuario, "proyecto": proyecto, "error": None},
    )


@router.post("/{proyecto_id}/editar")
def editar(
    proyecto_id: str,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    repo_proyectos.actualizar(proyecto_id, nombre, descripcion)
    return RedirectResponse(url="/proyectos", status_code=303)


@router.post("/{proyecto_id}/archivar")
def archivar(proyecto_id: str, usuario: dict = Depends(exigir_admin)):
    repo_proyectos.archivar(proyecto_id)
    return RedirectResponse(url="/proyectos", status_code=303)
