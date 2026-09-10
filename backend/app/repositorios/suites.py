"""Acceso a la coleccion suites (agrupan casos de prueba dentro de un proyecto)."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.database import obtener_db


def crear(proyecto_id: str, nombre: str, descripcion: str) -> str:
    db = obtener_db()
    resultado = db.suites.insert_one(
        {
            "proyecto_id": proyecto_id,
            "nombre": nombre.strip(),
            "descripcion": descripcion.strip(),
            "fecha_creacion": datetime.now(timezone.utc),
        }
    )
    return str(resultado.inserted_id)


def listar_por_proyecto(proyecto_id: str) -> list[dict]:
    db = obtener_db()
    return list(db.suites.find({"proyecto_id": proyecto_id}).sort("nombre", 1))


def obtener(suite_id: str) -> Optional[dict]:
    db = obtener_db()
    try:
        return db.suites.find_one({"_id": ObjectId(suite_id)})
    except Exception:
        return None


def actualizar(suite_id: str, nombre: str, descripcion: str) -> bool:
    db = obtener_db()
    try:
        resultado = db.suites.update_one(
            {"_id": ObjectId(suite_id)},
            {"$set": {"nombre": nombre.strip(), "descripcion": descripcion.strip()}},
        )
        return resultado.matched_count > 0
    except Exception:
        return False
