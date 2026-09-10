"""Carga la configuracion desde el archivo .env."""

import os

from dotenv import load_dotenv

load_dotenv()


def _requerido(clave: str) -> str:
    valor = os.getenv(clave)
    if not valor:
        raise RuntimeError(
            f"Falta la variable {clave} en el archivo .env. "
            "Copia .env.example como .env y completa tus valores."
        )
    return valor


MONGO_URI = _requerido("MONGO_URI")
JWT_SECRET = _requerido("JWT_SECRET")
JWT_ALGORITMO = "HS256"

SESION_HORAS = int(os.getenv("SESION_HORAS", "8"))
COOKIE_SESION = "gestor_qa_sesion"

# Roles validos. QA puede crear/editar; solo ADMIN puede archivar proyectos.
ROL_QA = "QA"
ROL_ADMIN = "ADMIN"
ROLES_VALIDOS = (ROL_QA, ROL_ADMIN)
