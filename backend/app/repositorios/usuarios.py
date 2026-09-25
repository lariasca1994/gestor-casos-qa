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
            "activo": True,
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


def listar_todos() -> list[dict]:
    """Todas las cuentas para la pantalla de gestion de usuarios (solo ADMIN,
    se valida en el router). Nunca devuelve password_hash."""
    db = obtener_db()
    return list(db.usuarios.find({}, {"password_hash": 0}).sort("nombre", 1))


def suspender(usuario_id: str) -> bool:
    """Marca la cuenta como inactiva: usuario_actual() la trata como si no
    hubiera sesion valida, con efecto inmediato (no hay que esperar a que
    expire el token). No se toca el rol ni se borra nada."""
    db = obtener_db()
    try:
        resultado = db.usuarios.update_one(
            {"_id": ObjectId(usuario_id)}, {"$set": {"activo": False}}
        )
        return resultado.matched_count > 0
    except Exception:
        return False


def reactivar(usuario_id: str) -> bool:
    db = obtener_db()
    try:
        resultado = db.usuarios.update_one(
            {"_id": ObjectId(usuario_id)}, {"$set": {"activo": True}}
        )
        return resultado.matched_count > 0
    except Exception:
        return False


def eliminar(usuario_id: str) -> bool:
    """Hard delete de la cuenta. A proposito NO cascadea sus proyectos,
    casos, ejecuciones ni defectos -- este es un proyecto de portafolio y
    borrar el historial de trabajo de alguien junto con su cuenta es mas
    riesgo que beneficio; esos documentos quedan huerfanos con el
    creado_por/ejecutado_por apuntando a un usuario que ya no existe, algo
    aceptable para esta demo (en un sistema real se reasignarian o se
    bloquearia el borrado mientras tenga proyectos)."""
    db = obtener_db()
    try:
        resultado = db.usuarios.delete_one({"_id": ObjectId(usuario_id)})
        return resultado.deleted_count > 0
    except Exception:
        return False
