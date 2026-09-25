"""Proyectos de ejemplo que se crean para cada cuenta nueva.

Cada usuario recibe su propia copia editable: son documentos normales con
su `creado_por`, no datos compartidos. Se insertan a traves de los
repositorios (no con insert_one directo) para que los campos coincidan
siempre con lo que esperan los listados, aunque el modelo cambie.
"""

import logging

from app.repositorios import casos_prueba as repo_casos
from app.repositorios import proyectos as repo_proyectos
from app.repositorios import suites as repo_suites

logger = logging.getLogger(__name__)

# Los pasos van sin numerar: la plantilla los numera con <ol>.
PROYECTOS_EJEMPLO = [
    {
        "nombre": "Portal de Facturacion Electronica",
        "descripcion": "Modulo web para generacion y consulta de facturas electronicas con validacion DIAN.",
        "suites": [
            {
                "nombre": "Autenticacion",
                "descripcion": "Casos de login, logout y control de sesion.",
                "casos": [
                    {
                        "titulo": "Login exitoso con credenciales validas",
                        "pasos": [
                            "Ingresar a la URL de login",
                            "Digitar usuario y contrasena validos",
                            "Clic en 'Iniciar sesion'",
                        ],
                        "resultado_esperado": "El sistema redirige al dashboard y muestra el nombre del usuario autenticado.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "Login con contrasena incorrecta",
                        "pasos": [
                            "Ingresar a la URL de login",
                            "Digitar usuario valido y contrasena incorrecta",
                            "Clic en 'Iniciar sesion'",
                        ],
                        "resultado_esperado": "El sistema muestra el mensaje 'Usuario o contrasena incorrectos' y no otorga acceso.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "Bloqueo de cuenta tras 5 intentos fallidos",
                        "pasos": [
                            "Intentar login con contrasena incorrecta cinco veces seguidas",
                        ],
                        "resultado_esperado": "La cuenta queda bloqueada temporalmente y se notifica al usuario.",
                        "prioridad": "Media",
                    },
                ],
            },
            {
                "nombre": "Emision de facturas",
                "descripcion": "Casos de creacion y validacion de facturas.",
                "casos": [
                    {
                        "titulo": "Emitir factura con datos completos y validos",
                        "pasos": [
                            "Ir a 'Nueva factura'",
                            "Diligenciar cliente, items y valores",
                            "Clic en 'Emitir'",
                        ],
                        "resultado_esperado": "La factura se emite, obtiene CUFE y aparece en el listado con estado 'Aceptada'.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "Intentar emitir factura sin NIT del cliente",
                        "pasos": [
                            "Ir a 'Nueva factura'",
                            "Dejar el campo NIT vacio",
                            "Clic en 'Emitir'",
                        ],
                        "resultado_esperado": "El sistema bloquea el envio y resalta el campo NIT como obligatorio.",
                        "prioridad": "Alta",
                    },
                ],
            },
        ],
    },
    {
        "nombre": "App de Reservas de Espacios",
        "descripcion": "Aplicacion para reservar salas y espacios comunes con calendario de disponibilidad.",
        "suites": [
            {
                "nombre": "Gestion de reservas",
                "descripcion": "Casos de creacion, edicion y cancelacion de reservas.",
                "casos": [
                    {
                        "titulo": "Crear reserva en horario disponible",
                        "pasos": [
                            "Seleccionar espacio",
                            "Elegir fecha y hora disponibles",
                            "Confirmar reserva",
                        ],
                        "resultado_esperado": "La reserva se crea y aparece en 'Mis reservas' con estado 'Confirmada'.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "Intentar reservar un horario ya ocupado",
                        "pasos": [
                            "Seleccionar espacio",
                            "Elegir fecha y hora ya reservadas por otro usuario",
                            "Confirmar reserva",
                        ],
                        "resultado_esperado": "El sistema muestra 'Horario no disponible' y no permite duplicar la reserva.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "Cancelar reserva con mas de 24h de anticipacion",
                        "pasos": [
                            "Ir a 'Mis reservas'",
                            "Seleccionar una reserva futura",
                            "Clic en 'Cancelar'",
                        ],
                        "resultado_esperado": "La reserva cambia a estado 'Cancelada' y el horario queda disponible nuevamente.",
                        "prioridad": "Media",
                    },
                ],
            },
        ],
    },
    {
        "nombre": "API de Gestion de Incidentes TI",
        "descripcion": "API REST para registro, asignacion y seguimiento de incidentes de soporte tecnico.",
        "suites": [
            {
                "nombre": "Endpoints de incidentes",
                "descripcion": "Casos sobre creacion y consulta de incidentes via API.",
                "casos": [
                    {
                        "titulo": "POST /incidentes crea un incidente valido",
                        "pasos": [
                            "Enviar POST a /incidentes con JSON valido (titulo, descripcion, prioridad)",
                            "Revisar la respuesta",
                        ],
                        "resultado_esperado": "Respuesta 201 Created con el ID del incidente generado.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "POST /incidentes sin token de autenticacion",
                        "pasos": [
                            "Enviar POST a /incidentes sin header Authorization",
                        ],
                        "resultado_esperado": "Respuesta 401 Unauthorized, no se crea el incidente.",
                        "prioridad": "Alta",
                    },
                    {
                        "titulo": "GET /incidentes/{id} con ID inexistente",
                        "pasos": [
                            "Enviar GET a /incidentes/000000000000000000000000",
                        ],
                        "resultado_esperado": "Respuesta 404 Not Found con mensaje de incidente no encontrado.",
                        "prioridad": "Media",
                    },
                    {
                        "titulo": "PATCH /incidentes/{id} cambia el estado a 'Resuelto'",
                        "pasos": [
                            "Enviar PATCH a /incidentes/{id} con {\"estado\": \"Resuelto\"}",
                            "Consultar el incidente",
                        ],
                        "resultado_esperado": "El incidente refleja el nuevo estado y la fecha de resolucion.",
                        "prioridad": "Media",
                    },
                ],
            },
        ],
    },
]


def ya_tiene_ejemplos(creado_por: str) -> bool:
    """True si el usuario ya tiene al menos uno de los proyectos de ejemplo."""
    nombres = [p["nombre"] for p in PROYECTOS_EJEMPLO]
    existentes = repo_proyectos.listar(solo_activos=False, creado_por=creado_por)
    return any(p.get("nombre") in nombres for p in existentes)


def crear_proyectos_ejemplo(creado_por: str) -> int:
    """Crea los proyectos de ejemplo para un usuario. Devuelve cuantos creo.

    Nunca lanza excepcion: si algo falla queda en el log y el registro del
    usuario continua igual. Perder los ejemplos es molesto; perder la cuenta
    recien creada, no.
    """
    creados = 0
    try:
        if ya_tiene_ejemplos(creado_por):
            return 0

        for proyecto in PROYECTOS_EJEMPLO:
            proyecto_id = repo_proyectos.crear(
                nombre=proyecto["nombre"],
                descripcion=proyecto["descripcion"],
                creado_por=creado_por,
            )
            creados += 1

            for suite in proyecto["suites"]:
                suite_id = repo_suites.crear(
                    proyecto_id=proyecto_id,
                    nombre=suite["nombre"],
                    descripcion=suite["descripcion"],
                )

                for caso in suite["casos"]:
                    repo_casos.crear(
                        proyecto_id=proyecto_id,
                        suite_id=suite_id,
                        titulo=caso["titulo"],
                        pasos=caso["pasos"],
                        resultado_esperado=caso["resultado_esperado"],
                        prioridad=caso["prioridad"],
                        creado_por=creado_por,
                    )
    except Exception:
        logger.exception(
            "No se pudieron crear los proyectos de ejemplo para el usuario %s.",
            creado_por,
        )

    return creados