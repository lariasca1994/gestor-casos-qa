"""Paginas de Casos de prueba, siempre dentro de una suite de un proyecto.
El acceso al proyecto (dueno o ADMIN) se valida en cada ruta via
proyecto_autorizado."""

import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dependencias import exigir_login, proyecto_autorizado
from app.repositorios import casos_prueba as repo_casos
from app.repositorios import ejecuciones as repo_ejecuciones
from app.repositorios import suites as repo_suites

router = APIRouter(prefix="/proyectos/{proyecto_id}/suites/{suite_id}/casos")
templates = Jinja2Templates(directory="app/templates")


# Quita un numero inicial propio ("1.", "2)", "3 -") si el usuario ya
# escribio los pasos numerados a mano: la plantilla los vuelve a numerar con
# <ol>, y sin esto quedaba "1. 1. Acceder..." duplicado.
_NUMERO_INICIAL = re.compile(r"^\s*\d+[.\)\-]\s*")


def _pasos_desde_texto(texto: str) -> list[str]:
    """Cada linea no vacia del textarea es un paso."""
    return [
        _NUMERO_INICIAL.sub("", linea).strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]


@router.get("", response_class=HTMLResponse)
def listar(
    request: Request,
    proyecto_id: str,
    suite_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "casos/lista.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": repo_suites.obtener(suite_id),
            "casos": repo_casos.listar_por_suite(suite_id),
            "ultimas_ejecuciones": repo_ejecuciones.ultimas_por_proyecto(proyecto_id),
        },
    )


@router.get("/nuevo", response_class=HTMLResponse)
def formulario_nuevo(
    request: Request,
    suite_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    return templates.TemplateResponse(
        "casos/formulario.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": repo_suites.obtener(suite_id),
            "caso": None,
            "pasos_texto": "",
            "error": None,
        },
    )


@router.post("/nuevo")
def crear(
    request: Request,
    proyecto_id: str,
    suite_id: str,
    titulo: str = Form(...),
    pasos: str = Form(""),
    resultado_esperado: str = Form(""),
    prioridad: str = Form("Media"),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    if not titulo.strip():
        return templates.TemplateResponse(
            "casos/formulario.html",
            {
                "request": request,
                "usuario": usuario,
                "proyecto": proyecto,
                "suite": repo_suites.obtener(suite_id),
                "caso": None,
                "pasos_texto": pasos,
                "error": "El titulo es obligatorio.",
            },
            status_code=400,
        )
    repo_casos.crear(
        proyecto_id=proyecto_id,
        suite_id=suite_id,
        titulo=titulo,
        pasos=_pasos_desde_texto(pasos),
        resultado_esperado=resultado_esperado,
        prioridad=prioridad,
        creado_por=str(usuario["_id"]),
    )
    return RedirectResponse(
        url=f"/proyectos/{proyecto_id}/suites/{suite_id}/casos", status_code=303
    )


@router.get("/{caso_id}/editar", response_class=HTMLResponse)
def formulario_editar(
    request: Request,
    suite_id: str,
    caso_id: str,
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    caso = repo_casos.obtener(caso_id)
    pasos_texto = "\n".join(caso["pasos"]) if caso else ""
    return templates.TemplateResponse(
        "casos/formulario.html",
        {
            "request": request,
            "usuario": usuario,
            "proyecto": proyecto,
            "suite": repo_suites.obtener(suite_id),
            "caso": caso,
            "pasos_texto": pasos_texto,
            "error": None,
        },
    )


@router.post("/{caso_id}/editar")
def editar(
    proyecto_id: str,
    suite_id: str,
    caso_id: str,
    titulo: str = Form(...),
    pasos: str = Form(""),
    resultado_esperado: str = Form(""),
    prioridad: str = Form("Media"),
    estado: str = Form("Activo"),
    usuario: dict = Depends(exigir_login),
    proyecto: dict = Depends(proyecto_autorizado),
):
    repo_casos.actualizar(
        caso_id=caso_id,
        titulo=titulo,
        pasos=_pasos_desde_texto(pasos),
        resultado_esperado=resultado_esperado,
        prioridad=prioridad,
        estado=estado,
    )
    return RedirectResponse(
        url=f"/proyectos/{proyecto_id}/suites/{suite_id}/casos", status_code=303
    )
