"""Acceso a la coleccion proyectos."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId

from app.database import obtener_db


def crear(nombre: str, descripcion: str, creado_por: str) -> str:
    db = obtener_db()
    resultado = db.proyectos.insert_one(
        {
            "nombre": nombre.strip(),
            "descripcion": descripcion.strip(),
            "creado_por": creado_por,
            "fecha_creacion": datetime.now(timezone.utc),
            "activo": True,
        }
    )
    return str(resultado.inserted_id)


def listar(solo_activos: bool = True, creado_por: Optional[str] = None) -> list[dict]:
    """creado_por=None trae todos (uso del ADMIN); con un id, solo los
    proyectos de ese usuario -- asi cada QA ve unicamente lo suyo."""
    db = obtener_db()
    filtro: dict = {"activo": True} if solo_activos else {}
    if creado_por is not None:
        filtro["creado_por"] = creado_por
    return list(db.proyectos.find(filtro).sort("nombre", 1))


def obtener(proyecto_id: str) -> Optional[dict]:
    db = obtener_db()
    try:
        return db.proyectos.find_one({"_id": ObjectId(proyecto_id)})
    except Exception:
        return None


def actualizar(proyecto_id: str, nombre: str, descripcion: str) -> bool:
    db = obtener_db()
    try:
        resultado = db.proyectos.update_one(
            {"_id": ObjectId(proyecto_id)},
            {"$set": {"nombre": nombre.strip(), "descripcion": descripcion.strip()}},
        )
        return resultado.matched_count > 0
    except Exception:
        return False


def archivar(proyecto_id: str) -> bool:
    """Solo ADMIN puede llamar a esto (se valida en el router). No se borra,
    se marca inactivo: conserva las suites/casos ya vinculados a el. Para el
    borrado real (irreversible) ver eliminar()."""
    db = obtener_db()
    try:
        resultado = db.proyectos.update_one(
            {"_id": ObjectId(proyecto_id)}, {"$set": {"activo": False}}
        )
        return resultado.matched_count > 0
    except Exception:
        return False


def eliminar(proyecto_id: str) -> bool:
    """Hard delete del proyecto y de todo lo que cuelga de el. Solo ADMIN
    puede llamar a esto (se valida en el router) -- a diferencia de
    archivar(), esto es irreversible.

    suites, casos_prueba, ejecuciones y defectos guardan todos un campo
    proyecto_id (string, no ObjectId) apuntando a este proyecto, asi que se
    puede borrar en cascada por ese campo directamente sin tener que ir
    coleccion por coleccion via suite_id/caso_id."""
    db = obtener_db()
    try:
        oid = ObjectId(proyecto_id)
    except Exception:
        return False
    db.defectos.delete_many({"proyecto_id": proyecto_id})
    db.ejecuciones.delete_many({"proyecto_id": proyecto_id})
    db.casos_prueba.delete_many({"proyecto_id": proyecto_id})
    db.suites.delete_many({"proyecto_id": proyecto_id})
    resultado = db.proyectos.delete_one({"_id": oid})
    return resultado.deleted_count > 0
