"""Hasheo de contrasenas y sesiones firmadas (JWT en cookie httponly).

Modulo nuevo para este proyecto (no reutiliza el de TaskFlow): bcrypt
directo, sin "pimiento" adicional, y un token con expiracion fija en vez de
inactividad deslizante -- mas simple, sigue siendo seguro para el alcance de
este portafolio.

Usa la libreria bcrypt directamente, sin pasar por passlib: passlib no se
actualiza desde 2020 y ya no es compatible con las versiones recientes de
bcrypt (rompe con un AttributeError/ValueError al arrancar). Sin esa capa
intermedia, el problema desaparece.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.config import COOKIE_SESION, JWT_ALGORITMO, JWT_SECRET, SESION_HORAS

# 12 rondas: costoso para fuerza bruta, imperceptible para el usuario real.
_RONDAS = 12


def cifrar(contrasena: str) -> str:
    """Devuelve el hash que se guarda en la base. Nunca se guarda texto plano."""
    hash_bytes = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt(rounds=_RONDAS))
    return hash_bytes.decode("utf-8")


def verificar(contrasena: str, hash_guardado: str) -> bool:
    """Compara una contrasena contra su hash. False tambien si el hash es invalido."""
    try:
        return bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def crear_token(usuario_id: str, email: str, rol: str) -> str:
    ahora = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": usuario_id,
            "email": email,
            "rol": rol,
            "iat": int(ahora.timestamp()),
            "exp": ahora + timedelta(hours=SESION_HORAS),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITMO,
    )


def leer_token(token: str) -> dict | None:
    """Devuelve la carga del token si es valido y no ha expirado, si no None."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITMO])
    except jwt.PyJWTError:
        return None


__all__ = ["cifrar", "verificar", "crear_token", "leer_token", "COOKIE_SESION"]
