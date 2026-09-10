"""Acceso a la coleccion defectos, siempre vinculados a una ejecucion fallida."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.database import obtener_db

SEVERIDADES = ("Critica", "Alta", "Media", "Baja")
ESTADOS = ("Abierto", "En progreso", "Cerrado")


def crear(
    ejecucion_id: str,
    caso_id: str,
    proyecto_id: str,
    titulo: str,
    descripcion: str,
    severidad: str,
    creado_por: str,
) -> str:
    db = obtener_db()
    resultado = db.defectos.insert_one(
        {
            "ejecucion_id": ejecucion_id,
            "caso_id": caso_id,
            "proyecto_id": proyecto_id,
            "titulo": titulo.strip(),
            "descripcion": descripcion.strip(),
            "severidad": severidad if severidad in SEVERIDADES else "Media",
            "estado": "Abierto",
            "creado_por": creado_por,
            "fecha_creacion": datetime.now(timezone.utc),
        }
    )
    return str(resultado.inserted_id)


def listar_por_proyecto(proyecto_id: str) -> list[dict]:
    db = obtener_db()
    return list(db.defectos.find({"proyecto_id": proyecto_id}).sort("fecha_creacion", -1))


def contar_abiertos_por_severidad(proyecto_id: str) -> dict[str, int]:
    """{severidad: cantidad} solo para defectos que no estan Cerrado."""
    db = obtener_db()
    pipeline = [
        {"$match": {"proyecto_id": proyecto_id, "estado": {"$ne": "Cerrado"}}},
        {"$group": {"_id": "$severidad", "total": {"$sum": 1}}},
    ]
    conteo = {severidad: 0 for severidad in SEVERIDADES}
    for doc in db.defectos.aggregate(pipeline):
        conteo[doc["_id"]] = doc["total"]
    return conteo


def existe_para_ejecucion(ejecucion_id: str) -> bool:
    db = obtener_db()
    return db.defectos.count_documents({"ejecucion_id": ejecucion_id}) > 0


def obtener(defecto_id: str) -> Optional[dict]:
    db = obtener_db()
    try:
        return db.defectos.find_one({"_id": ObjectId(defecto_id)})
    except Exception:
        return None


def actualizar_estado(defecto_id: str, estado: str) -> bool:
    db = obtener_db()
    try:
        resultado = db.defectos.update_one(
            {"_id": ObjectId(defecto_id)},
            {"$set": {"estado": estado if estado in ESTADOS else "Abierto"}},
        )
        return resultado.matched_count > 0
    except Exception:
        return False
