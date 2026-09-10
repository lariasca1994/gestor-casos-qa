"""Conexion a MongoDB e indices de las colecciones."""

from pymongo import ASCENDING, MongoClient
from pymongo.database import Database

from app.config import MONGO_URI

_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
_db: Database = _client.get_default_database()


def obtener_db() -> Database:
    return _db


def verificar_conexion() -> None:
    """Falla rapido y con un mensaje claro si Mongo no responde."""
    _client.admin.command("ping")


def asegurar_indices() -> None:
    """Crea los indices necesarios si todavia no existen (no destruye nada)."""
    db = obtener_db()
    db.usuarios.create_index([("email", ASCENDING)], unique=True)
    db.proyectos.create_index([("nombre", ASCENDING)])
    db.suites.create_index([("proyecto_id", ASCENDING)])
    db.casos_prueba.create_index([("suite_id", ASCENDING)])
    db.casos_prueba.create_index([("proyecto_id", ASCENDING)])
    db.ejecuciones.create_index([("caso_id", ASCENDING)])
    db.defectos.create_index([("ejecucion_id", ASCENDING)])
