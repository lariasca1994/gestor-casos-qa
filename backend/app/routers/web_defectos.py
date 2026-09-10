"""Defectos: se crean desde una ejecucion fallida, se gestionan por proyecto.
El acceso al proyecto (dueno o ADMIN) se valida en cada ruta via
proyecto_autorizado."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import exigir_login, proyecto_autorizado
from app.repositorios import casos_prueba as repo_casos
from app.repositorios import defectos as repo_defectos
from app.repositorios import ejecuciones as repo_ejecuciones
from app.repositorios import suites as repo_suites

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get(
    "/proyectos/{proyecto_id}/suites/{suite_id}/casos/{caso_id}/ejecuciones/{ejecucion_id}/defecto/nuevo",
    response_class=HTMLResponse,
)
def formulario_nuevo(
    request: Request,
    suite_id: str,
    caso_id: str,
    ejecucion_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "defectos/formulario.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": repo_suites.obtener(suite_id),
            "caso": repo_casos.obtener(caso_id),
            "ejecucion": repo_ejecuciones.obtener(ejecucion_id),
            "error": None,
        },
    )


@router.post("/proyectos/{proyecto_id}/suites/{suite_id}/casos/{caso_id}/ejecuciones/{ejecucion_id}/defecto/nuevo")
def crear(
    request: Request,
    proyecto_id: str,
    suite_id: str,
    caso_id: str,
    ejecucion_id: str,
    titulo: str = Form(...),
    descripcion: str = Form(""),
    severidad: str = Form("Media"),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    if not titulo.strip():
        return templates.TemplateResponse(
            "defectos/formulario.html",
            {
                "request": request,
                "usuario": usuario,
                "proyecto": proyecto,
                "suite": repo_suites.obtener(suite_id),
                "caso": repo_casos.obtener(caso_id),
                "ejecucion": repo_ejecuciones.obtener(ejecucion_id),
                "error": "El titulo es obligatorio.",
            },
            status_code=400,
        )
    repo_defectos.crear(
        ejecucion_id=ejecucion_id,
        caso_id=caso_id,
        proyecto_id=proyecto_id,
        titulo=titulo,
        descripcion=descripcion,
        severidad=severidad,
        creado_por=str(usuario["_id"]),
    )
    return RedirectResponse(url=f"/proyectos/{proyecto_id}/defectos", status_code=303)


@router.get("/proyectos/{proyecto_id}/defectos", response_class=HTMLResponse)
def listar(
    request: Request,
    proyecto_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "defectos/lista.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "defectos": repo_defectos.listar_por_proyecto(proyecto_id),
        },
    )


@router.post("/proyectos/{proyecto_id}/defectos/{defecto_id}/estado")
def cambiar_estado(
    proyecto_id: str,
    defecto_id: str,
    estado: str = Form(...),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    repo_defectos.actualizar_estado(defecto_id, estado)
    return RedirectResponse(url=f"/proyectos/{proyecto_id}/defectos", status_code=303)
