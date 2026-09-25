"""Acceso a la coleccion casos_prueba."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.database import obtener_db

PRIORIDADES = ("Alta", "Media", "Baja")
ESTADOS = ("Activo", "Obsoleto")


def crear(
    proyecto_id: str,
    suite_id: str,
    titulo: str,
    pasos: list[str],
    resultado_esperado: str,
    prioridad: str,
    creado_por: str,
) -> str:
    db = obtener_db()
    resultado = db.casos_prueba.insert_one(
        {
            "proyecto_id": proyecto_id,
            "suite_id": suite_id,
            "titulo": titulo.strip(),
            "pasos": pasos,
            "resultado_esperado": resultado_esperado.strip(),
            "prioridad": prioridad if prioridad in PRIORIDADES else "Media",
            "estado": "Activo",
            "creado_por": creado_por,
            "fecha_creacion": datetime.now(timezone.utc),
        }
    )
    return str(resultado.inserted_id)


def listar_por_suite(suite_id: str) -> list[dict]:
    db = obtener_db()
    return list(db.casos_prueba.find({"suite_id": suite_id}).sort("titulo", 1))


def contar_por_proyecto(proyecto_id: str) -> int:
    return obtener_db().casos_prueba.count_documents({"proyecto_id": proyecto_id})


def obtener(caso_id: str) -> Optional[dict]:
    db = obtener_db()
    try:
        return db.casos_prueba.find_one({"_id": ObjectId(caso_id)})
    except Exception:
        return None


def actualizar(
    caso_id: str,
    titulo: str,
    pasos: list[str],
    resultado_esperado: str,
    prioridad: str,
    estado: str,
) -> bool:
    db = obtener_db()
    try:
        resultado = db.casos_prueba.update_one(
            {"_id": ObjectId(caso_id)},
            {
                "$set": {
                    "titulo": titulo.strip(),
                    "pasos": pasos,
                    "resultado_esperado": resultado_esperado.strip(),
                    "prioridad": prioridad if prioridad in PRIORIDADES else "Media",
                    "estado": estado if estado in ESTADOS else "Activo",
                }
            },
        )
        return resultado.matched_count > 0
    except Exception:
        return False


def eliminar(caso_id: str) -> bool:
    """Hard delete del caso junto con sus ejecuciones y los defectos
    vinculados a ellas, para no dejar huerfanos. Se permite a dueno o ADMIN
    (se valida en el router con proyecto_autorizado), igual que editar."""
    db = obtener_db()
    try:
        oid = ObjectId(caso_id)
    except Exception:
        return False
    db.defectos.delete_many({"caso_id": caso_id})
    db.ejecuciones.delete_many({"caso_id": caso_id})
    resultado = db.casos_prueba.delete_one({"_id": oid})
    return resultado.deleted_count > 0
