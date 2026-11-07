"""Recuperación de la cuenta: "Olvidé mi contraseña" y "Perdí mi autenticador"."""

import re
import time
from datetime import datetime, timedelta, timezone

from app import mfa
from app.config import COOKIE_SESION
from app.seguridad import COOKIE_MFA, crear_token, crear_token_mfa, crear_token_recuperacion

from conftest import CLAVE

NUEVA = "clave-nueva-456"


def _con_totp(base):
    """Cuenta con app autenticadora activa (el método correo NO está activo)."""
    usuario = base.crear()
    mfa.iniciar_totp(usuario)
    base.actualizar_mfa(str(usuario["_id"]), {"mfa.totp": base.leer(usuario["_id"])["mfa"]["totp_pendiente"],
                                              "mfa.totp_pendiente": None, "mfa.preferido": "totp"})
    return base.leer(usuario["_id"])


def _codigo_app(cifrado: str) -> str:
    return mfa._totp(mfa._descifrar(cifrado), int(time.time()) // mfa._PASO)


def _con_pase(cliente, usuario, recuperado=False):
    cliente.cookies.set(COOKIE_MFA, crear_token_mfa(str(usuario["_id"]), usuario["password_hash"], recuperado))


def _codigo_correo(base) -> str:
    return re.search(r"\b(\d{6})\b", base.correos[-1]["texto"]).group(1)


# ── Olvidé mi contraseña ─────────────────────────────────────────────────────


def test_recuperar_responde_igual_exista_o_no_la_cuenta(cliente, base):
    base.crear()
    existe = cliente.post("/recuperar", data={"email": "usuario@ejemplo.com"})
    no_existe = cliente.post("/recuperar", data={"email": "nadie@ejemplo.com"})
    assert existe.status_code == no_existe.status_code == 200
    assert existe.text == no_existe.text
    assert len(base.correos) == 1


def test_enlace_sirve_una_sola_vez_y_vence(cliente, base):
    usuario = base.crear()
    token = crear_token_recuperacion(str(usuario["_id"]), usuario["password_hash"], 30)
    ok = cliente.post("/restablecer", data={"token": token, "contrasena": NUEVA, "confirmar": NUEVA})
    assert ok.status_code == 200
    otra = cliente.post("/restablecer", data={"token": token, "contrasena": "otra-clave-789", "confirmar": "otra-clave-789"})
    assert otra.status_code == 400  # segundo uso: la huella de la contraseña ya cambió

    vencido = crear_token_recuperacion(str(usuario["_id"]), base.leer(usuario["_id"])["password_hash"], -1)
    assert "no es válido o ya venció" in cliente.get(f"/restablecer?token={vencido}").text


def test_paso_dos_solo_pide_nueva_y_confirmar(cliente, base):
    usuario = base.crear()
    token = crear_token_recuperacion(str(usuario["_id"]), usuario["password_hash"], 30)
    pagina = cliente.get(f"/restablecer?token={token}").text
    campos = set(re.findall(r'<input[^>]*name="([^"]+)"', pagina))
    assert campos == {"token", "contrasena", "confirmar"}
    distinta = cliente.post("/restablecer", data={"token": token, "contrasena": NUEVA, "confirmar": "no-coincide-1"})
    assert distinta.status_code == 400


def test_restablecer_cierra_sesiones_y_mantiene_la_verificacion(cliente, base):
    usuario = _con_totp(base)
    totp_antes = usuario["mfa"]["totp"]
    sesion = crear_token(str(usuario["_id"]), usuario["email"], usuario["rol"], usuario["password_hash"])
    cliente.cookies.set(COOKIE_SESION, sesion)
    assert cliente.get("/cuenta/contrasena").status_code == 200

    token = crear_token_recuperacion(str(usuario["_id"]), usuario["password_hash"], 30)
    cliente.post("/restablecer", data={"token": token, "contrasena": NUEVA, "confirmar": NUEVA})

    cliente.cookies.clear()
    cliente.cookies.set(COOKIE_SESION, sesion)  # la sesión vieja, desde otro equipo
    assert cliente.get("/cuenta/contrasena").headers.get("location") == "/login"
    despues = base.leer(usuario["_id"])
    assert despues["mfa"]["totp"] == totp_antes and mfa.configurado(despues)

    cliente.cookies.clear()
    ingreso = cliente.post("/login", data={"email": "usuario@ejemplo.com", "contrasena": NUEVA})
    assert ingreso.headers["location"] == "/verificacion"  # sigue pidiendo el segundo paso
    assert COOKIE_SESION not in ingreso.cookies


def test_cambiar_contrasena_cierra_las_otras_sesiones_y_mantiene_esta(cliente, base):
    usuario = base.crear()
    vieja = crear_token(str(usuario["_id"]), usuario["email"], usuario["rol"], usuario["password_hash"])
    cliente.cookies.set(COOKIE_SESION, vieja)
    r = cliente.post("/cuenta/contrasena", data={"actual": CLAVE, "contrasena": NUEVA, "confirmar": NUEVA})
    assert r.status_code == 200
    assert cliente.get("/cuenta/contrasena").status_code == 200  # esta sesión sigue (cookie nueva)
    cliente.cookies.clear()
    cliente.cookies.set(COOKIE_SESION, vieja)
    assert cliente.get("/cuenta/contrasena").status_code == 303


# ── Perdí mi autenticador ────────────────────────────────────────────────────


def test_enlace_siempre_visible_en_la_pantalla_del_codigo(cliente, base):
    usuario = _con_totp(base)
    _con_pase(cliente, usuario)
    assert "Perdí mi autenticador" in cliente.get("/verificacion").text
    base.actualizar_mfa(str(usuario["_id"]), {"mfa.correo": True, "mfa.preferido": "correo"})
    assert "Perdí mi autenticador" in cliente.get("/verificacion").text


def test_envia_codigo_al_correo_aunque_el_metodo_correo_no_este_activo(cliente, base):
    usuario = _con_totp(base)
    assert "correo" not in mfa.metodos_activos(usuario)
    _con_pase(cliente, usuario)
    r = cliente.post("/verificacion/perdi-autenticador")
    assert r.status_code == 200
    assert base.correos[-1]["destino"] == "usuario@ejemplo.com"
    assert "Gestor de casos de prueba QA" in base.correos[-1]["asunto"]
    expira = base.leer(usuario["_id"])["mfa"]["rec_codigo"]["expira"]
    restante = expira - datetime.now(timezone.utc)
    assert timedelta(minutes=14) < restante <= timedelta(minutes=15)


def test_limite_de_envios(cliente, base):
    usuario = _con_totp(base)
    _con_pase(cliente, usuario)
    for _ in range(3):
        assert cliente.post("/verificacion/perdi-autenticador").status_code == 200
    assert cliente.post("/verificacion/perdi-autenticador").status_code == 429
    assert len(base.correos) == 3


def test_codigo_vencido_no_sirve(base):
    usuario = _con_totp(base)
    mfa.enviar_codigo_recuperacion(usuario)
    codigo = _codigo_correo(base)
    guardado = base.leer(usuario["_id"])["mfa"]["rec_codigo"]
    base.actualizar_mfa(str(usuario["_id"]), {"mfa.rec_codigo": {**guardado, "expira": datetime.now(timezone.utc) - timedelta(seconds=1)}})
    assert not mfa.verificar_codigo_recuperacion(base.leer(usuario["_id"]), codigo)


def test_cinco_errores_bloquean_quince_minutos(cliente, base):
    usuario = _con_totp(base)
    _con_pase(cliente, usuario)
    cliente.post("/verificacion/perdi-autenticador")
    codigo = _codigo_correo(base)
    errado = "000000" if codigo != "000000" else "111111"
    for _ in range(5):
        assert cliente.post("/verificacion/recuperar", data={"codigo": errado}).status_code == 401
    bloqueo = base.leer(usuario["_id"])["mfa"]["rec_bloqueo_hasta"]
    assert 14 * 60 < bloqueo - time.time() <= 15 * 60
    # Ni el código correcto ni uno nuevo funcionan durante el bloqueo.
    assert cliente.post("/verificacion/recuperar", data={"codigo": codigo}).status_code == 401
    assert cliente.post("/verificacion/perdi-autenticador").status_code == 429


def test_acertar_el_codigo_no_abre_sesion_hasta_activar_la_app_nueva(cliente, base):
    usuario = _con_totp(base)
    totp_viejo = usuario["mfa"]["totp"]
    _con_pase(cliente, usuario)
    cliente.post("/verificacion/perdi-autenticador")
    r = cliente.post("/verificacion/recuperar", data={"codigo": _codigo_correo(base)})
    assert r.status_code == 200
    assert "mfa-qr" in r.text and "/verificacion/reemplazar" in r.text
    assert COOKIE_SESION not in r.cookies
    assert cliente.get("/cuenta/contrasena").status_code == 303  # sin sesión
    estado = base.leer(usuario["_id"])["mfa"]
    assert estado["totp"] == totp_viejo  # la app anterior sigue hasta confirmar la nueva

    # Recargar la página muestra el mismo QR pendiente, no otro.
    assert cliente.get("/verificacion").status_code == 200
    assert base.leer(usuario["_id"])["mfa"]["totp_pendiente"] == estado["totp_pendiente"]

    errado = cliente.post("/verificacion/reemplazar", data={"codigo": "000000"})
    assert errado.status_code == 401 and COOKIE_SESION not in errado.cookies
    assert base.leer(usuario["_id"])["mfa"]["totp"] == totp_viejo

    ok = cliente.post("/verificacion/reemplazar", data={"codigo": _codigo_app(estado["totp_pendiente"])})
    assert ok.status_code == 303 and ok.headers["location"] == "/proyectos"
    assert COOKIE_SESION in ok.cookies
    final = base.leer(usuario["_id"])["mfa"]
    assert final["totp"] == estado["totp_pendiente"] and final["totp"] != totp_viejo
    assert final["totp_pendiente"] is None and final["preferido"] == "totp"


def test_reemplazar_sin_validar_el_correo_no_cambia_nada(cliente, base):
    usuario = _con_totp(base)
    mfa.iniciar_totp(base.leer(usuario["_id"]))
    pendiente = base.leer(usuario["_id"])["mfa"]["totp_pendiente"]
    _con_pase(cliente, usuario)  # pase normal, sin el código del correo
    r = cliente.post("/verificacion/reemplazar", data={"codigo": _codigo_app(pendiente)})
    assert COOKIE_SESION not in r.cookies
    assert base.leer(usuario["_id"])["mfa"]["totp"] == usuario["mfa"]["totp"]


def test_el_pase_deja_de_servir_si_cambia_la_contrasena(cliente, base):
    usuario = _con_totp(base)
    _con_pase(cliente, usuario, recuperado=True)
    base.actualizar_contrasena(str(usuario["_id"]), NUEVA)
    assert cliente.get("/verificacion").headers.get("location") == "/login"


def test_nombre_visible_en_el_qr_sin_tocar_la_clave_interna(base):
    usuario = base.crear()
    datos = mfa.iniciar_totp(usuario)
    assert mfa.EMISOR == "Gestor de casos de prueba QA"
    assert datos["secreto"]
    # La etiqueta interna de cifrado no cambió: los TOTP ya configurados siguen sirviendo.
    assert b"GestorCasosQA.MFA.v1" in open(mfa.__file__, "rb").read()
    assert mfa._descifrar(base.leer(usuario["_id"])["mfa"]["totp_pendiente"]) == datos["secreto"]


def test_remitente_y_correo_con_el_nombre_visible(monkeypatch):
    """El nombre del remitente sale del código (no de la nube); la dirección sí es la variable."""
    import json

    from app import correo as real  # sin el fixture "base": enviar() es el real
    monkeypatch.setattr(real, "BREVO_API_KEY", "clave-ficticia")
    monkeypatch.setattr(real, "BREVO_REMITENTE", "remitente@ejemplo.com")
    enviado = {}

    class Respuesta:
        status = 201
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def falso_urlopen(pedido, timeout):
        enviado.update(json.loads(pedido.data))
        return Respuesta()

    monkeypatch.setattr(real.urllib.request, "urlopen", falso_urlopen)
    assert real.enviar("usuario@ejemplo.com", "Ana Pérez", "Asunto", "texto", "<p>hola</p>")
    assert enviado["sender"] == {"email": "remitente@ejemplo.com", "name": "Gestor de casos de prueba QA"}
    assert "Gestor de casos de prueba QA</span>" in enviado["htmlContent"]
    assert "Correo automático de Gestor de casos de prueba QA" in enviado["htmlContent"]
