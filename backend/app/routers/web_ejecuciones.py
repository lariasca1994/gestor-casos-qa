"""Registro de ejecuciones de un caso de prueba y su historial. El acceso al
proyecto (dueno o ADMIN) se valida en cada ruta via proyecto_autorizado."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import exigir_login, proyecto_autorizado
from app.repositorios import casos_prueba as repo_casos
from app.repositorios import ejecuciones as repo_ejecuciones
from app.repositorios import suites as repo_suites
from app.repositorios import usuarios as repo_usuarios

router = APIRouter(prefix="/proyectos/{proyecto_id}/suites/{suite_id}/casos/{caso_id}/ejecuciones")
templates = Jinja2Templates(directory="app/templates")


def _historial_con_nombres(caso_id: str) -> list[dict]:
    historial = []
    for ejecucion in repo_ejecuciones.listar_por_caso(caso_id):
        usuario = repo_usuarios.buscar_por_id(ejecucion["ejecutado_por"])
        ejecucion["ejecutado_por_nombre"] = usuario["nombre"] if usuario else "?"
        historial.append(ejecucion)
    return historial


@router.get("", response_class=HTMLResponse)
def listar(
    request: Request,
    suite_id: str,
    caso_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "ejecuciones/lista.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": repo_suites.obtener(suite_id),
            "caso": repo_casos.obtener(caso_id),
            "historial": _historial_con_nombres(caso_id),
        },
    )


@router.post("")
def registrar(
    proyecto_id: str,
    suite_id: str,
    caso_id: str,
    resultado: str = Form(...),
    comentario: str = Form(""),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    repo_ejecuciones.crear(
        caso_id=caso_id,
        proyecto_id=proyecto_id,
        resultado=resultado,
        comentario=comentario,
        ejecutado_por=str(usuario["_id"]),
    )
    return RedirectResponse(
        url=f"/proyectos/{proyecto_id}/suites/{suite_id}/casos/{caso_id}/ejecuciones",
        status_code=303,
    )
