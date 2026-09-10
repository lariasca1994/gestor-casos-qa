"""Registro, inicio y cierre de sesion.

El registro publico siempre crea cuentas con rol QA. La cuenta ADMIN de
revision se crea aparte con app.comandos.crear_admin (ver README) -- mismo
criterio que en PRPagos: el rol de administrador no sale de un formulario
publico.
"""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import COOKIE_SESION, SESION_HORAS
from app.dependencias import usuario_actual
from app.repositorios.usuarios import buscar_por_correo, crear_usuario
from app.seguridad import crear_token, verificar

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/registro", response_class=HTMLResponse)
def formulario_registro(request: Request):
    if usuario_actual(request):
        return RedirectResponse(url="/proyectos", status_code=303)
    return templates.TemplateResponse(
        "registro.html", {"request": request, "error": None}
    )


@router.post("/registro", response_class=HTMLResponse)
def procesar_registro(
    request: Request,
    email: str = Form(...),
    nombre: str = Form(...),
    contrasena: str = Form(...),
    confirmar: str = Form(...),
):
    error = None
    if contrasena != confirmar:
        error = "Las contrasenas no coinciden."
    elif len(contrasena) < 8:
        error = "La contrasena debe tener al menos 8 caracteres."
    elif buscar_por_correo(email):
        error = "Ya existe una cuenta con ese correo."

    if error:
        return templates.TemplateResponse(
            "registro.html",
            {"request": request, "error": error},
            status_code=400,
        )

    crear_usuario(email=email, nombre=nombre, contrasena=contrasena)
    return RedirectResponse(url="/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def formulario_login(request: Request):
    if usuario_actual(request):
        return RedirectResponse(url="/proyectos", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
def procesar_login(request: Request, email: str = Form(...), contrasena: str = Form(...)):
    usuario = buscar_por_correo(email)
    if not usuario or not verificar(contrasena, usuario["password_hash"]):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Correo o contrasena incorrectos."},
            status_code=400,
        )

    token = crear_token(str(usuario["_id"]), usuario["email"], usuario["rol"])
    respuesta = RedirectResponse(url="/proyectos", status_code=303)
    respuesta.set_cookie(
        COOKIE_SESION,
        token,
        httponly=True,
        samesite="lax",
        max_age=SESION_HORAS * 3600,
    )
    return respuesta


@router.get("/logout")
def logout():
    respuesta = RedirectResponse(url="/", status_code=303)
    respuesta.delete_cookie(COOKIE_SESION)
    return respuesta
