"""Acceso a la coleccion usuarios."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.config import ROL_QA
from app.database import obtener_db
from app.seguridad import cifrar


def crear_usuario(email: str, nombre: str, contrasena: str, rol: str = ROL_QA) -> str:
    db = obtener_db()
    resultado = db.usuarios.insert_one(
        {
            "email": email.strip().lower(),
            "nombre": nombre.strip(),
            "password_hash": cifrar(contrasena),
            "rol": rol,
            "fecha_creacion": datetime.now(timezone.utc),
        }
    )
    return str(resultado.inserted_id)


def buscar_por_correo(email: str) -> Optional[dict]:
    db = obtener_db()
    return db.usuarios.find_one({"email": email.strip().lower()})


def buscar_por_id(usuario_id: str) -> Optional[dict]:
    db = obtener_db()
    try:
        return db.usuarios.find_one({"_id": ObjectId(usuario_id)})
    except Exception:
        return None


def contar_usuarios() -> int:
    return obtener_db().usuarios.count_documents({})
