"""Crea los proyectos de ejemplo para las cuentas que ya existen.

Las cuentas nuevas los reciben solas al registrarse (ver web_auth). Este
comando es solo para las que se crearon antes de ese cambio. Se puede
correr varias veces sin duplicar nada: salta a quien ya los tenga.

Uso:
    cd backend
    python -m app.comandos.poblar_ejemplos
"""

from app.database import obtener_db
from app.datos_ejemplo import crear_proyectos_ejemplo, ya_tiene_ejemplos


def main() -> None:
    db = obtener_db()
    usuarios = list(db.usuarios.find({}, {"_id": 1, "email": 1}))

    if not usuarios:
        print("No hay usuarios en la base.")
        return

    poblados = saltados = 0

    for usuario in usuarios:
        usuario_id = str(usuario["_id"])
        email = usuario.get("email", usuario_id)

        if ya_tiene_ejemplos(usuario_id):
            print(f"  {email}: ya tenia los ejemplos, se salta.")
            saltados += 1
            continue

        creados = crear_proyectos_ejemplo(creado_por=usuario_id)
        if creados:
            print(f"  {email}: {creados} proyecto(s) de ejemplo creados.")
            poblados += 1
        else:
            print(f"  {email}: no se crearon (revisa el log de errores).")

    print(f"\nListo. {poblados} cuenta(s) pobladas, {saltados} sin cambios.")


if __name__ == "__main__":
    main()