"""
Script de seed para gestor-casos-qa
Inserta 3 proyectos, sus suites y casos de prueba reales en MongoDB.

ANTES DE CORRER:
1. pip install pymongo python-dotenv
2. Crea un archivo .env en la misma carpeta con:
     MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net
3. Nombres de colecciones y FKs ya confirmados contra backend/app (asegurar_indices()).
"""

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "gestor_casos_qa"

COL_PROYECTOS = "proyectos"
COL_SUITES = "suites"
COL_CASOS = "casos_prueba"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

now = lambda: datetime.now(timezone.utc)

# ---------------------------------------------------------------------------
# DATOS: 3 proyectos, cada uno con 1-2 suites y varios casos de prueba reales
# ---------------------------------------------------------------------------

data = [
    {
        "proyecto": {"nombre": "Portal de Facturación Electrónica",
                     "descripcion": "Módulo web para generación y consulta de facturas electrónicas con validación DIAN."},
        "suites": [
            {
                "suite": {"nombre": "Autenticación", "descripcion": "Casos de login, logout y control de sesión."},
                "casos": [
                    {"titulo": "Login exitoso con credenciales válidas",
                     "pasos": "1. Ingresar a la URL de login\n2. Digitar usuario y contraseña válidos\n3. Clic en 'Iniciar sesión'",
                     "resultado_esperado": "El sistema redirige al dashboard y muestra el nombre del usuario autenticado.",
                     "prioridad": "Alta"},
                    {"titulo": "Login con contraseña incorrecta",
                     "pasos": "1. Ingresar a la URL de login\n2. Digitar usuario válido y contraseña incorrecta\n3. Clic en 'Iniciar sesión'",
                     "resultado_esperado": "El sistema muestra el mensaje 'Usuario o contraseña incorrectos' y no otorga acceso.",
                     "prioridad": "Alta"},
                    {"titulo": "Bloqueo de cuenta tras 5 intentos fallidos",
                     "pasos": "1. Intentar login con contraseña incorrecta 5 veces seguidas",
                     "resultado_esperado": "La cuenta queda bloqueada temporalmente y se notifica al usuario.",
                     "prioridad": "Media"},
                ],
            },
            {
                "suite": {"nombre": "Emisión de facturas", "descripcion": "Casos de creación y validación de facturas."},
                "casos": [
                    {"titulo": "Emitir factura con datos completos y válidos",
                     "pasos": "1. Ir a 'Nueva factura'\n2. Diligenciar cliente, ítems y valores\n3. Clic en 'Emitir'",
                     "resultado_esperado": "La factura se emite, obtiene CUFE y aparece en el listado con estado 'Aceptada'.",
                     "prioridad": "Alta"},
                    {"titulo": "Intentar emitir factura sin NIT del cliente",
                     "pasos": "1. Ir a 'Nueva factura'\n2. Dejar el campo NIT vacío\n3. Clic en 'Emitir'",
                     "resultado_esperado": "El sistema bloquea el envío y resalta el campo NIT como obligatorio.",
                     "prioridad": "Alta"},
                ],
            },
        ],
    },
    {
        "proyecto": {"nombre": "App de Reservas de Espacios",
                     "descripcion": "Aplicación para reservar salas y espacios comunes con calendario de disponibilidad."},
        "suites": [
            {
                "suite": {"nombre": "Gestión de reservas", "descripcion": "Casos de creación, edición y cancelación de reservas."},
                "casos": [
                    {"titulo": "Crear reserva en horario disponible",
                     "pasos": "1. Seleccionar espacio\n2. Elegir fecha y hora disponibles\n3. Confirmar reserva",
                     "resultado_esperado": "La reserva se crea y aparece en 'Mis reservas' con estado 'Confirmada'.",
                     "prioridad": "Alta"},
                    {"titulo": "Intentar reservar un horario ya ocupado",
                     "pasos": "1. Seleccionar espacio\n2. Elegir fecha y hora ya reservadas por otro usuario\n3. Confirmar reserva",
                     "resultado_esperado": "El sistema muestra 'Horario no disponible' y no permite duplicar la reserva.",
                     "prioridad": "Alta"},
                    {"titulo": "Cancelar reserva con más de 24h de anticipación",
                     "pasos": "1. Ir a 'Mis reservas'\n2. Seleccionar una reserva futura\n3. Clic en 'Cancelar'",
                     "resultado_esperado": "La reserva cambia a estado 'Cancelada' y el horario queda disponible nuevamente.",
                     "prioridad": "Media"},
                ],
            },
        ],
    },
    {
        "proyecto": {"nombre": "API de Gestión de Incidentes TI",
                     "descripcion": "API REST para registro, asignación y seguimiento de incidentes de soporte técnico."},
        "suites": [
            {
                "suite": {"nombre": "Endpoints de incidentes", "descripcion": "Casos sobre creación y consulta de incidentes vía API."},
                "casos": [
                    {"titulo": "POST /incidentes crea un incidente válido",
                     "pasos": "1. Enviar POST a /incidentes con JSON válido (titulo, descripcion, prioridad)\n2. Revisar respuesta",
                     "resultado_esperado": "Respuesta 201 Created con el ID del incidente generado.",
                     "prioridad": "Alta"},
                    {"titulo": "POST /incidentes sin token de autenticación",
                     "pasos": "1. Enviar POST a /incidentes sin header Authorization",
                     "resultado_esperado": "Respuesta 401 Unauthorized, no se crea el incidente.",
                     "prioridad": "Alta"},
                    {"titulo": "GET /incidentes/{id} con ID inexistente",
                     "pasos": "1. Enviar GET a /incidentes/000000000000000000000000",
                     "resultado_esperado": "Respuesta 404 Not Found con mensaje de incidente no encontrado.",
                     "prioridad": "Media"},
                    {"titulo": "PATCH /incidentes/{id} cambia el estado a 'Resuelto'",
                     "pasos": "1. Enviar PATCH a /incidentes/{id} con {\"estado\": \"Resuelto\"}\n2. Consultar el incidente",
                     "resultado_esperado": "El incidente refleja el nuevo estado y la fecha de resolución.",
                     "prioridad": "Media"},
                ],
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# INSERCIÓN
# ---------------------------------------------------------------------------

def main():
    total_proyectos = total_suites = total_casos = 0

    for bloque in data:
        proyecto_doc = {**bloque["proyecto"], "creado_en": now()}
        proyecto_id = db[COL_PROYECTOS].insert_one(proyecto_doc).inserted_id
        total_proyectos += 1

        for suite_bloque in bloque["suites"]:
            suite_doc = {**suite_bloque["suite"], "proyecto_id": proyecto_id, "creado_en": now()}
            suite_id = db[COL_SUITES].insert_one(suite_doc).inserted_id
            total_suites += 1

            for caso in suite_bloque["casos"]:
                caso_doc = {**caso, "suite_id": suite_id, "proyecto_id": proyecto_id, "creado_en": now()}
                db[COL_CASOS].insert_one(caso_doc)
                total_casos += 1

    print(f"Listo: {total_proyectos} proyectos, {total_suites} suites, {total_casos} casos de prueba insertados en '{DB_NAME}'.")


if __name__ == "__main__":
    main()