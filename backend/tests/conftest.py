"""Pruebas sin base de datos real: la colección usuarios se simula en memoria.

Se corren desde backend/:  python -m pytest tests
"""

import copy
import os
import sys
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
os.chdir(BACKEND)  # las plantillas se cargan con ruta relativa (app/templates)
sys.path.insert(0, str(BACKEND))
# Valores ficticios solo para pruebas: MongoClient no se conecta hasta usarse.
os.environ["MONGO_URI"] = "mongodb://127.0.0.1:1/pruebas"
os.environ["JWT_SECRET"] = "clave-de-pruebas-que-no-se-usa-en-ningun-lado"
os.environ["BREVO_API_KEY"] = ""

from bson import ObjectId  # noqa: E402

from app import auditoria, correo, dependencias, mfa  # noqa: E402
from app.routers import web_auth  # noqa: E402
from app.seguridad import cifrar  # noqa: E402

CLAVE = "clave-original-123"


class BaseFalsa:
    def __init__(self):
        self.usuarios: dict[str, dict] = {}
        self.correos: list[dict] = []
        self.eventos: list[str] = []

    def crear(self, **extra) -> dict:
        _id = ObjectId()
        self.usuarios[str(_id)] = {
            "_id": _id, "email": "usuario@ejemplo.com", "nombre": "Ana Pérez", "rol": "QA", "activo": True,
            "password_hash": cifrar(CLAVE), **extra,
        }
        return self.leer(str(_id))

    def leer(self, usuario_id: str) -> dict | None:
        u = self.usuarios.get(str(usuario_id))
        return copy.deepcopy(u) if u else None

    def por_correo(self, email: str) -> dict | None:
        for u in self.usuarios.values():
            if u["email"] == email.strip().lower():
                return copy.deepcopy(u)
        return None

    def actualizar_mfa(self, usuario_id: str, cambios: dict) -> None:
        u = self.usuarios[str(usuario_id)]
        for clave, valor in cambios.items():
            u.setdefault("mfa", {})[clave.removeprefix("mfa.")] = copy.deepcopy(valor)

    def actualizar_contrasena(self, usuario_id: str, contrasena: str) -> None:
        self.usuarios[str(usuario_id)]["password_hash"] = cifrar(contrasena)


@pytest.fixture
def base(monkeypatch) -> BaseFalsa:
    b = BaseFalsa()
    monkeypatch.setattr(mfa, "actualizar_mfa", b.actualizar_mfa)
    monkeypatch.setattr(auditoria, "registrar", lambda tipo, usuario: b.eventos.append(tipo))
    monkeypatch.setattr(correo, "enviar", lambda destino, nombre, asunto, texto, html: b.correos.append(
        {"destino": destino, "asunto": asunto, "texto": texto}) or True)
    monkeypatch.setattr(web_auth, "buscar_por_id", b.leer)
    monkeypatch.setattr(web_auth, "buscar_por_correo", b.por_correo)
    monkeypatch.setattr(web_auth, "actualizar_contrasena", b.actualizar_contrasena)
    monkeypatch.setattr(dependencias, "buscar_por_id", b.leer)
    return b


@pytest.fixture
def cliente(base):
    from fastapi.testclient import TestClient

    from app.main import app

    # Sin "with": no corre el arranque (que haría ping a MongoDB).
    return TestClient(app, base_url="http://testserver", follow_redirects=False)
