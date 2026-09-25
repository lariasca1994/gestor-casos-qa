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


def eliminar(suite_id: str) -> bool:
    """Hard delete de la suite y de sus casos, para no dejar huerfanos. Se
    permite a dueno o ADMIN (se valida en el router con proyecto_autorizado),
    igual que editar.

    casos_prueba tiene suite_id, pero ejecuciones y defectos solo guardan
    caso_id (no suite_id), asi que primero hay que ubicar los ids de los
    casos de esta suite para poder borrar en cascada tambien sus
    ejecuciones/defectos."""
    db = obtener_db()
    try:
        oid = ObjectId(suite_id)
    except Exception:
        return False
    caso_ids = [
        str(caso["_id"]) for caso in db.casos_prueba.find({"suite_id": suite_id}, {"_id": 1})
    ]
    if caso_ids:
        db.defectos.delete_many({"caso_id": {"$in": caso_ids}})
        db.ejecuciones.delete_many({"caso_id": {"$in": caso_ids}})
    db.casos_prueba.delete_many({"suite_id": suite_id})
    resultado = db.suites.delete_one({"_id": oid})
    return resultado.deleted_count > 0
