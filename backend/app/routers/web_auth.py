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

from app import correo, mfa
from app.config import COOKIE_SESION, RECUPERAR_MINUTOS, SESION_HORAS, URL_PUBLICA
from app.datos_ejemplo import crear_proyectos_ejemplo
from app.dependencias import exigir_login, usuario_actual
from app.repositorios.usuarios import actualizar_contrasena, buscar_por_correo, buscar_por_id, crear_usuario
from app.seguridad import (
    COOKIE_MFA,
    MFA_MINUTOS,
    crear_token,
    crear_token_mfa,
    leer_token_mfa,
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
    # Antes de entrar, la cuenta elige su verificación en dos pasos.
    return _pase_mfa(buscar_por_id(usuario_id))


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

    if not usuario.get("activo", True):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Esta cuenta está suspendida."}, status_code=403
        )
    # La contraseña sola no abre sesión: falta el segundo paso.
    if mfa.preferido(usuario) == "correo":
        mfa.enviar_codigo(usuario)
    return _pase_mfa(usuario)


def _abrir_sesion(usuario: dict) -> RedirectResponse:
    token = crear_token(str(usuario["_id"]), usuario["email"], usuario["rol"])
    respuesta = RedirectResponse(url="/proyectos", status_code=303)
    respuesta.set_cookie(
        COOKIE_SESION,
        token,
        httponly=True,
        samesite="lax",
        max_age=SESION_HORAS * 3600,
    )
    respuesta.delete_cookie(COOKIE_MFA)
    return respuesta


# ── Verificación en dos pasos ──────────────────────────────────────────────


def _pase_mfa(usuario: dict) -> RedirectResponse:
    respuesta = RedirectResponse(url="/verificacion", status_code=303)
    respuesta.set_cookie(COOKIE_MFA, crear_token_mfa(str(usuario["_id"])), httponly=True, samesite="lax",
                         max_age=MFA_MINUTOS * 60)
    return respuesta


def _usuario_en_verificacion(request: Request) -> dict | None:
    usuario_id = leer_token_mfa(request.cookies.get(COOKIE_MFA))
    usuario = buscar_por_id(usuario_id) if usuario_id else None
    return usuario if usuario and usuario.get("activo", True) else None


def _vencido() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)


def _pantalla_mfa(request: Request, usuario: dict, metodo: str | None = None, status_code: int = 200, **contexto):
    if not mfa.configurado(usuario):
        return templates.TemplateResponse(
            "mfa_elegir.html", {"request": request, "metodos": mfa.METODOS, **contexto}, status_code=status_code)
    metodo = metodo if metodo in mfa.metodos_activos(usuario) else mfa.preferido(usuario)
    otros = [m for m in mfa.metodos_activos(usuario) if m != metodo]
    return templates.TemplateResponse(
        "mfa_verificar.html",
        {"request": request, "metodo": metodo, "otro": otros[0] if otros else None, "metodos": mfa.METODOS,
         "email": usuario["email"], **contexto},
        status_code=status_code,
    )


def _iniciar_metodo(request: Request, usuario: dict, metodo: str, accion: str, vista: str, **contexto):
    if metodo == "totp":
        return _confirmar_metodo(request, usuario, metodo, accion, vista, app=mfa.iniciar_totp(usuario), **contexto)
    if not mfa.enviar_codigo(usuario):
        contexto["error"] = "Pediste varios códigos seguidos. Espera unos minutos."
    return _confirmar_metodo(request, usuario, "correo", accion, vista, **contexto)


def _confirmar_metodo(request: Request, usuario: dict, metodo: str, accion: str, vista: str, **contexto):
    plantilla = "mfa_confirmar.html" if vista == "acceso" else "cuenta_seguridad.html"
    base = {"request": request, "metodo": metodo, "accion": accion, "metodos": mfa.METODOS, "email": usuario["email"]}
    if vista != "acceso":
        base.update(_contexto_seguridad(usuario))
    return templates.TemplateResponse(plantilla, {**base, **contexto}, status_code=401 if "error" in contexto else 200)


def _contexto_seguridad(usuario: dict) -> dict:
    return {"usuario": usuario, "activos": mfa.metodos_activos(usuario), "preferido": mfa.preferido(usuario)}


@router.get("/verificacion", response_class=HTMLResponse)
def form_verificacion(request: Request, metodo: str | None = None):
    usuario = _usuario_en_verificacion(request)
    return _pantalla_mfa(request, usuario, metodo) if usuario else _vencido()


@router.post("/verificacion", response_class=HTMLResponse)
def procesar_verificacion(request: Request, metodo: str = Form(...), codigo: str = Form(...)):
    usuario = _usuario_en_verificacion(request)
    if not usuario:
        return _vencido()
    if not mfa.verificar(usuario, metodo, codigo):
        return _pantalla_mfa(request, usuario, metodo, status_code=401, error="El código no es correcto o ya venció.")
    return _abrir_sesion(usuario)


@router.post("/verificacion/correo", response_class=HTMLResponse)
def reenviar_codigo(request: Request):
    usuario = _usuario_en_verificacion(request)
    if not usuario:
        return _vencido()
    if not mfa.enviar_codigo(usuario):
        return _pantalla_mfa(request, usuario, "correo", error="Pediste varios códigos seguidos. Espera unos minutos.")
    return _pantalla_mfa(request, usuario, "correo", exito=f"Te enviamos un código a {usuario['email']}.")


@router.post("/verificacion/configurar", response_class=HTMLResponse)
def configurar_metodo(request: Request, metodo: str = Form(...)):
    usuario = _usuario_en_verificacion(request)
    if not usuario:
        return _vencido()
    return _iniciar_metodo(request, usuario, metodo, "/verificacion/activar", "acceso")


@router.post("/verificacion/activar", response_class=HTMLResponse)
def activar_metodo(request: Request, metodo: str = Form(...), codigo: str = Form(...)):
    usuario = _usuario_en_verificacion(request)
    if not usuario:
        return _vencido()
    if mfa.configurado(usuario):  # ya tiene uno: este paso es solo para la primera vez
        return _pantalla_mfa(request, usuario)
    activado = mfa.activar_totp(usuario, codigo) if metodo == "totp" else mfa.activar_correo(usuario, codigo)
    if not activado:
        return _confirmar_metodo(request, usuario, metodo, "/verificacion/activar", "acceso",
                                 error="El código no es correcto o ya venció.")
    return _abrir_sesion(usuario)


@router.get("/cuenta/seguridad", response_class=HTMLResponse)
def form_seguridad(request: Request, usuario: dict = Depends(exigir_login)):
    return templates.TemplateResponse(
        "cuenta_seguridad.html", {"request": request, "metodos": mfa.METODOS, **_contexto_seguridad(usuario)})


@router.post("/cuenta/seguridad/agregar", response_class=HTMLResponse)
def agregar_metodo(request: Request, metodo: str = Form(...), usuario: dict = Depends(exigir_login)):
    if metodo not in mfa.METODOS or metodo in mfa.metodos_activos(usuario):
        return RedirectResponse(url="/cuenta/seguridad", status_code=303)
    return _iniciar_metodo(request, usuario, metodo, "/cuenta/seguridad/activar", "cuenta")


@router.post("/cuenta/seguridad/activar", response_class=HTMLResponse)
def activar_en_perfil(request: Request, metodo: str = Form(...), codigo: str = Form(...),
                      usuario: dict = Depends(exigir_login)):
    activado = mfa.activar_totp(usuario, codigo) if metodo == "totp" else mfa.activar_correo(usuario, codigo)
    if not activado:
        return _confirmar_metodo(request, usuario, metodo, "/cuenta/seguridad/activar", "cuenta",
                                 error="El código no es correcto o ya venció.")
    return templates.TemplateResponse("cuenta_seguridad.html", {
        "request": request, "metodos": mfa.METODOS, **_contexto_seguridad(usuario),
        "exito": f"{mfa.METODOS[metodo]} quedó activada como segundo paso.",
    })


@router.post("/cuenta/seguridad/preferido")
def cambiar_preferido(metodo: str = Form(...), usuario: dict = Depends(exigir_login)):
    mfa.elegir_preferido(usuario, metodo)
    return RedirectResponse(url="/cuenta/seguridad", status_code=303)


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
