"""Punto de entrada: arma la app, monta estaticos, registra rutas y maneja
los redireccionamientos de sesion (login/permisos) en un solo lugar."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import asegurar_indices, verificar_conexion
from app.dependencias import NoAutorizado, RequiereLogin, usuario_actual
from app.routers import (
    web_auth,
    web_casos,
    web_dashboard,
    web_defectos,
    web_ejecuciones,
    web_proyectos,
    web_suites,
    web_usuarios,
)

app = FastAPI(title="Gestor de Casos de Prueba QA")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def al_arrancar() -> None:
    verificar_conexion()
    asegurar_indices()
    print("[GestorQA] Conexion a MongoDB verificada, indices listos.")


@app.exception_handler(RequiereLogin)
def redirigir_a_login(request: Request, exc: RequiereLogin):
    return RedirectResponse(url="/login", status_code=303)


@app.exception_handler(NoAutorizado)
def no_autorizado(request: Request, exc: NoAutorizado):
    return HTMLResponse(
        "<h1>403</h1><p>Tu cuenta no tiene permiso para esto.</p>"
        '<p><a href="/proyectos">Volver</a></p>',
        status_code=403,
    )


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return templates.TemplateResponse(
        "inicio.html", {"request": request, "usuario": usuario_actual(request)}
    )


app.include_router(web_auth.router)
app.include_router(web_proyectos.router)
app.include_router(web_suites.router)
app.include_router(web_casos.router)
app.include_router(web_ejecuciones.router)
app.include_router(web_defectos.router)
app.include_router(web_dashboard.router)
app.include_router(web_usuarios.router)
