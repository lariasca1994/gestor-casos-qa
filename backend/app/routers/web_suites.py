"""Paginas de Suites de prueba, siempre dentro de un proyecto. El acceso al
proyecto (dueno o ADMIN) se valida en cada ruta via proyecto_autorizado."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import exigir_login, proyecto_autorizado
from app.repositorios import suites as repo_suites

router = APIRouter(prefix="/proyectos/{proyecto_id}/suites")
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def listar(
    request: Request,
    proyecto_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "suites/lista.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suites": repo_suites.listar_por_proyecto(proyecto_id),
        },
    )


@router.get("/nueva", response_class=HTMLResponse)
def formulario_nueva(
    request: Request,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "suites/formulario.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": None,
            "error": None,
        },
    )


@router.post("/nueva")
def crear(
    request: Request,
    proyecto_id: str,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    if not nombre.strip():
        return templates.TemplateResponse(
            "suites/formulario.html",
            {
                "request": request,
                "usuario": usuario,
                "proyecto": proyecto,
                "suite": None,
                "error": "El nombre es obligatorio.",
            },
            status_code=400,
        )
    repo_suites.crear(proyecto_id, nombre, descripcion)
    return RedirectResponse(url=f"/proyectos/{proyecto_id}/suites", status_code=303)


@router.get("/{suite_id}/editar", response_class=HTMLResponse)
def formulario_editar(
    request: Request,
    suite_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "suites/formulario.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": repo_suites.obtener(suite_id),
            "error": None,
        },
    )


@router.post("/{suite_id}/editar")
def editar(
    proyecto_id: str,
    suite_id: str,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    repo_suites.actualizar(suite_id, nombre, descripcion)
    return RedirectResponse(url=f"/proyectos/{proyecto_id}/suites", status_code=303)
