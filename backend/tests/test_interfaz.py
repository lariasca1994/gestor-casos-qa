"""Interfaz: menú lateral, aplicación instalable (PWA) y página 404 propia."""

from app.config import COOKIE_SESION
from app.seguridad import crear_token


def _sesion(cliente, base, **extra):
    usuario = base.crear(**extra)
    cliente.cookies.set(COOKIE_SESION, crear_token(str(usuario["_id"]), usuario["email"], usuario["rol"], usuario["password_hash"]))
    return usuario


def test_menu_lateral_con_las_mismas_opciones(cliente, base):
    _sesion(cliente, base)
    html = cliente.get("/cuenta/contrasena").text
    assert 'class="menu-nav"' in html and 'href="/proyectos"' in html
    assert 'href="/cuenta/seguridad"' in html and 'href="/logout"' in html
    # El enlace de salida conserva el nombre (lo usa el script de capturas del manual).
    assert "Salir</span><span class=\"oculto\"> (Ana Pérez)</span>" in html
    assert 'class="hoja-mas"' in html
    # Contraseña marcada como la pantalla actual.
    assert 'class="menu-cuenta activo" href="/cuenta/contrasena"' in html
    # Un QA no ve Usuarios.
    assert 'href="/admin/usuarios"' not in html


def test_admin_ve_usuarios_en_el_menu_y_en_la_hoja(cliente, base):
    _sesion(cliente, base, rol="ADMIN")
    html = cliente.get("/cuenta/contrasena").text
    assert html.count('href="/admin/usuarios"') == 2


def test_pwa_service_worker_manifiesto_y_sin_conexion(cliente):
    sw = cliente.get("/sw.js")
    assert sw.status_code == 200 and "javascript" in sw.headers["content-type"]
    assert sw.headers["cache-control"] == "no-cache"
    # Nunca guarda páginas con datos: solo la cáscara.
    assert "/proyectos" not in sw.text
    manifiesto = cliente.get("/manifest.webmanifest")
    assert manifiesto.status_code == 200 and manifiesto.json()["display"] == "standalone"
    for icono in manifiesto.json()["icons"]:
        assert cliente.get(icono["src"]).status_code == 200
    sin_red = cliente.get("/offline.html")
    assert sin_red.status_code == 200 and "Sin conexión" in sin_red.text


def test_404_propia_sin_consultar_la_base(cliente):
    r = cliente.get("/no-existe-esta-ruta")
    assert r.status_code == 404
    assert "Este caso no está en ninguna suite" in r.text
    assert "/no-existe-esta-ruta" in r.text


def test_otros_errores_http_siguen_igual(cliente):
    r = cliente.post("/favicon.ico")
    assert r.status_code == 405
