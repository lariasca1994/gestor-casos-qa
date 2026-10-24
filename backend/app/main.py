"""Punto de entrada: arma la app, monta estaticos, registra rutas y maneja
los redireccionamientos de sesion (login/permisos) en un solo lugar."""

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

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
    # Si MongoDB no responde al arrancar, la app arranca igual: las peticiones
    # muestran la pantalla de mantenimiento en vez de un 502 de la plataforma.
    try:
        verificar_conexion()
        asegurar_indices()
        print("[GestorQA] Conexion a MongoDB verificada, indices listos.")
    except (ServerSelectionTimeoutError, ConnectionFailure) as error:
        print(f"[GestorQA] MongoDB no disponible al arrancar: {type(error).__name__}")


@app.exception_handler(ServerSelectionTimeoutError)
@app.exception_handler(ConnectionFailure)
def base_no_disponible(request: Request, exc: Exception):
    """MongoDB apagado o inalcanzable: pantalla de mantenimiento (503), no un error genérico."""
    return templates.TemplateResponse(request, "mantenimiento.html", {"request": request}, status_code=503, headers={"Retry-After": "300"}
    )


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
    # La portada de acceso es la primera pantalla, igual que en el resto
    # del portafolio; con sesion abierta se va directo a los proyectos.
    if usuario_actual(request):
        return RedirectResponse(url="/proyectos", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"request": request, "error": None})


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Los navegadores lo piden en la raiz aunque la pagina declare otro icono.
    return FileResponse("app/static/iconos/favicon.ico")


app.include_router(web_auth.router)
app.include_router(web_proyectos.router)
app.include_router(web_suites.router)
app.include_router(web_casos.router)
app.include_router(web_ejecuciones.router)
app.include_router(web_defectos.router)
app.include_router(web_dashboard.router)
app.include_router(web_usuarios.router)
