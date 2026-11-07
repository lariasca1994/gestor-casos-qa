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

import hashlib
import hmac
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


def crear_token(usuario_id: str, email: str, rol: str, hash_guardado: str) -> str:
    """La sesion lleva la huella de la contrasena: al cambiarla o restablecerla,
    todas las sesiones abiertas con la anterior dejan de valer."""
    ahora = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": usuario_id,
            "email": email,
            "rol": rol,
            "h": _huella(hash_guardado),
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


# ── Recuperación de cuenta ─────────────────────────────────────────────────
# Enlace firmado, con vencimiento y de un solo uso: lleva la huella de la
# contraseña actual (al cambiarla deja de servir) y una audiencia propia, así
# que leer_token (sesiones) lo rechaza.
_AUDIENCIA_RECUPERAR = "recuperar"


def _huella(hash_guardado: str) -> str:
    return hashlib.sha256((hash_guardado or "").encode()).hexdigest()[:24]


def crear_token_recuperacion(usuario_id: str, hash_guardado: str, minutos: int) -> str:
    return jwt.encode(
        {"sub": usuario_id, "h": _huella(hash_guardado), "aud": _AUDIENCIA_RECUPERAR,
         "exp": datetime.now(timezone.utc) + timedelta(minutes=minutos)},
        JWT_SECRET, algorithm=JWT_ALGORITMO,
    )


def leer_token_recuperacion(token: str) -> tuple[str, str] | None:
    try:
        carga = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITMO], audience=_AUDIENCIA_RECUPERAR)
        return str(carga["sub"]), str(carga["h"])
    except (jwt.PyJWTError, KeyError):
        return None


def huella_coincide(hash_guardado: str, huella: str) -> bool:
    return hmac.compare_digest(_huella(hash_guardado), huella)


# ── Paso intermedio de la verificación en dos pasos ────────────────────────
# Pase de 10 minutos entre la contraseña y el código; leer_token (sesiones) lo
# rechaza por llevar audiencia. Lleva la huella de la contraseña (al cambiarla
# deja de servir) y "rec" cuando ya se validó el código de "Perdí mi
# autenticador": ese pase solo sirve para activar la app nueva.
_AUDIENCIA_MFA = "mfa"
COOKIE_MFA = "gestor_qa_mfa"
MFA_MINUTOS = 10


def crear_token_mfa(usuario_id: str, hash_guardado: str, recuperado: bool = False) -> str:
    return jwt.encode(
        {"sub": usuario_id, "h": _huella(hash_guardado), "rec": recuperado, "aud": _AUDIENCIA_MFA,
         "exp": datetime.now(timezone.utc) + timedelta(minutes=MFA_MINUTOS)},
        JWT_SECRET, algorithm=JWT_ALGORITMO,
    )


def leer_token_mfa(token: str | None) -> dict | None:
    """Devuelve {"sub", "h", "rec"} si el pase es valido, si no None."""
    if not token:
        return None
    try:
        carga = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITMO], audience=_AUDIENCIA_MFA)
        return {"sub": str(carga["sub"]), "h": str(carga["h"]), "rec": bool(carga.get("rec"))}
    except (jwt.PyJWTError, KeyError):
        return None
