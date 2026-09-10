"""Acceso a la coleccion ejecuciones (historial de corridas de un caso)."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.database import obtener_db

RESULTADOS = ("Passed", "Failed", "Blocked", "Skipped")


def crear(
    caso_id: str,
    proyecto_id: str,
    resultado: str,
    comentario: str,
    ejecutado_por: str,
) -> str:
    db = obtener_db()
    resultado_doc = db.ejecuciones.insert_one(
        {
            "caso_id": caso_id,
            "proyecto_id": proyecto_id,
            "resultado": resultado if resultado in RESULTADOS else "Skipped",
            "comentario": comentario.strip(),
            "ejecutado_por": ejecutado_por,
            "fecha": datetime.now(timezone.utc),
        }
    )
    return str(resultado_doc.inserted_id)


def listar_por_caso(caso_id: str) -> list[dict]:
    db = obtener_db()
    return list(db.ejecuciones.find({"caso_id": caso_id}).sort("fecha", -1))


def ultima_por_caso(caso_id: str) -> Optional[dict]:
    db = obtener_db()
    return db.ejecuciones.find_one({"caso_id": caso_id}, sort=[("fecha", -1)])


def ultimas_por_proyecto(proyecto_id: str) -> dict:
    """Devuelve {caso_id: ultima_ejecucion} para todos los casos ya ejecutados
    del proyecto -- una sola consulta, util para listas y el dashboard."""
    db = obtener_db()
    pipeline = [
        {"$match": {"proyecto_id": proyecto_id}},
        {"$sort": {"fecha": -1}},
        {"$group": {"_id": "$caso_id", "ejecucion": {"$first": "$$ROOT"}}},
    ]
    return {doc["_id"]: doc["ejecucion"] for doc in db.ejecuciones.aggregate(pipeline)}


def listar_por_proyecto(proyecto_id: str) -> list[dict]:
    db = obtener_db()
    return list(db.ejecuciones.find({"proyecto_id": proyecto_id}))


def obtener(ejecucion_id: str) -> Optional[dict]:
    db = obtener_db()
    try:
        return db.ejecuciones.find_one({"_id": ObjectId(ejecucion_id)})
    except Exception:
        return None
