"""Crea (o asciende a) una cuenta ADMIN. No pasa por el formulario publico.

Uso:
    cd backend
    python -m app.comandos.crear_admin correo@ejemplo.com "Nombre" contrasena
"""

import sys

from app.config import ROL_ADMIN
from app.database import obtener_db
from app.repositorios.usuarios import buscar_por_correo, crear_usuario
from app.seguridad import cifrar


def main() -> None:
    if len(sys.argv) != 4:
        print(__doc__)
        raise SystemExit(1)

    email, nombre, contrasena = sys.argv[1], sys.argv[2], sys.argv[3]
    existente = buscar_por_correo(email)

    if existente:
        obtener_db().usuarios.update_one(
            {"_id": existente["_id"]},
            {"$set": {"rol": ROL_ADMIN, "password_hash": cifrar(contrasena)}},
        )
        print(f"Cuenta existente {email} ascendida a ADMIN.")
    else:
        crear_usuario(email=email, nombre=nombre, contrasena=contrasena, rol=ROL_ADMIN)
        print(f"Cuenta ADMIN {email} creada.")


if __name__ == "__main__":
    main()
