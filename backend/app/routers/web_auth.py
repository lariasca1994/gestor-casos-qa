"""Registro, inicio y cierre de sesion.

El registro publico siempre crea cuentas con rol QA. La cuenta ADMIN de
revision se crea aparte con app.comandos.crear_admin (ver README) -- mismo
criterio que en PRPagos: el rol de administrador no sale de un formulario
publico.
"""

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import html
import threading
import time

from fastapi import Depends

from app import correo
from app.config import COOKIE_SESION, RECUPERAR_MINUTOS, SESION_HORAS, URL_PUBLICA
from app.datos_ejemplo import crear_proyectos_ejemplo
from app.dependencias import exigir_login, usuario_actual
from app.repositorios.usuarios import actualizar_contrasena, buscar_por_correo, buscar_por_id, crear_usuario
from app.seguridad import (
    crear_token,
    crear_token_recuperacion,
    huella_coincide,
    leer_token_recuperacion,
    verificar,
)

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

    usuario_id = crear_usuario(email=email, nombre=nombre, contrasena=contrasena)
    # La cuenta nueva arranca con proyectos de ejemplo para que haya algo
    # que explorar. No lanza excepciones: si falla, el registro sigue igual.
    crear_proyectos_ejemplo(creado_por=usuario_id)
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


# ── Recuperar y cambiar la contraseña ──────────────────────────────────────

_RESPUESTA_RECUPERAR = (
    "Si el correo pertenece a una cuenta, te enviamos un enlace para crear una contraseña nueva. "
    "Revisa tu bandeja (y la carpeta de spam)."
)
_ENVIOS: dict[str, list[float]] = {}
_CANDADO = threading.Lock()


def _puede_enviar(email: str) -> bool:
    """Máximo 3 enlaces cada 15 minutos por correo (no bloquea el ingreso)."""
    ahora = time.time()
    with _CANDADO:
        recientes = [t for t in _ENVIOS.get(email, []) if ahora - t < 15 * 60]
        _ENVIOS[email] = recientes if len(recientes) >= 3 else recientes + [ahora]
        return len(recientes) < 3


@router.get("/recuperar", response_class=HTMLResponse)
def formulario_recuperar(request: Request):
    return templates.TemplateResponse("recuperar.html", {"request": request, "error": None})


@router.post("/recuperar", response_class=HTMLResponse)
def procesar_recuperar(request: Request, email: str = Form(...)):
    email = email.strip().lower()
    usuario = buscar_por_correo(email)
    if usuario and usuario.get("activo", True) and _puede_enviar(email):
        token = crear_token_recuperacion(str(usuario["_id"]), usuario["password_hash"], RECUPERAR_MINUTOS)
        enlace = f"{URL_PUBLICA}/restablecer?token={token}"
        nombre = usuario.get("nombre", "")
        correo.enviar(
            usuario["email"], nombre, "Restablece tu contraseña · Gestor QA",
            f"Hola {nombre},\n\nPara crear una contraseña nueva abre este enlace (vence en "
            f"{RECUPERAR_MINUTOS} minutos y sirve una vez):\n\n{enlace}\n\n"
            "Si no fuiste tú, ignora este correo: tu contraseña no cambia.",
            f"<p>Hola {html.escape(nombre)},</p><p>Para crear una contraseña nueva en <strong>Gestor QA</strong>:</p>"
            f'<p><a href="{enlace}" style="background:#0d9488;color:#fff;padding:10px 18px;border-radius:6px;'
            f'text-decoration:none">Crear contraseña nueva</a></p><p>El enlace vence en {RECUPERAR_MINUTOS} '
            "minutos y sirve una sola vez. Si no fuiste tú, ignora este correo.</p>",
        )
    return templates.TemplateResponse(
        "recuperar.html", {"request": request, "error": None, "exito": _RESPUESTA_RECUPERAR}
    )


@router.get("/restablecer", response_class=HTMLResponse)
def formulario_restablecer(request: Request, token: str = ""):
    error = None if leer_token_recuperacion(token) else "El enlace no es válido o ya venció. Pide uno nuevo."
    return templates.TemplateResponse("restablecer.html", {"request": request, "token": token, "error": error})


@router.post("/restablecer", response_class=HTMLResponse)
def procesar_restablecer(
    request: Request,
    token: str = Form(...),
    contrasena: str = Form(...),
    confirmar: str = Form(...),
):
    leido = leer_token_recuperacion(token)
    usuario = buscar_por_id(leido[0]) if leido else None
    error = None
    if not usuario or not usuario.get("activo", True) or not huella_coincide(usuario["password_hash"], leido[1]):
        error = "El enlace no es válido o ya venció. Pide uno nuevo."
    elif contrasena != confirmar:
        error = "Las contrasenas no coinciden."
    elif len(contrasena) < 8:
        error = "La contrasena debe tener al menos 8 caracteres."
    if error:
        return templates.TemplateResponse(
            "restablecer.html", {"request": request, "token": token, "error": error}, status_code=400
        )
    actualizar_contrasena(str(usuario["_id"]), contrasena)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None, "exito": "Tu contraseña quedó actualizada. Ya puedes ingresar."},
    )


@router.get("/cuenta/contrasena", response_class=HTMLResponse)
def formulario_cambiar_contrasena(request: Request, usuario: dict = Depends(exigir_login)):
    return templates.TemplateResponse(
        "cuenta_contrasena.html", {"request": request, "usuario": usuario, "error": None}
    )


@router.post("/cuenta/contrasena", response_class=HTMLResponse)
def cambiar_contrasena(
    request: Request,
    actual: str = Form(...),
    contrasena: str = Form(...),
    confirmar: str = Form(...),
    usuario: dict = Depends(exigir_login),
):
    error = None
    if not verificar(actual, usuario["password_hash"]):
        error = "La contraseña actual no es correcta."
    elif contrasena != confirmar:
        error = "Las contrasenas no coinciden."
    elif len(contrasena) < 8:
        error = "La contrasena debe tener al menos 8 caracteres."
    elif contrasena == actual:
        error = "La contraseña nueva debe ser distinta de la actual."
    if error:
        return templates.TemplateResponse(
            "cuenta_contrasena.html", {"request": request, "usuario": usuario, "error": error}, status_code=400
        )
    actualizar_contrasena(str(usuario["_id"]), contrasena)
    return templates.TemplateResponse(
        "cuenta_contrasena.html",
        {"request": request, "usuario": usuario, "error": None, "exito": "Tu contraseña quedó actualizada."},
    )
