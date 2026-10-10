# Gestor de Casos de Prueba QA

<p>
  <a href="https://immxew65sfxj7nubwzlszdimfi0qegzc.lambda-url.us-east-1.on.aws/"><img src="docs/demo-badge.svg" alt="Abrir la demo en vivo" height="32"></a>
  <a href="https://frontend-nine-topaz-99.vercel.app"><img src="https://portafolio-status.onrender.com/api/status/gestor-casos-qa/badge.svg" alt="Estado en vivo del proyecto" height="32"></a>
  <a href="https://d4i3vsgw7xwmh.cloudfront.net"><img src="https://portafolio-status.onrender.com/api/status/gestor-casos-qa/qa-badge.svg" alt="Fecha y resultado de la última prueba E2E" height="32"></a>
</p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-3D72D7?style=for-the-badge&logo=htmx&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)

## Contenido

1. [Presentación](#1-presentación)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Arquitectura](#3-arquitectura)
4. [Plataformas y su función](#4-plataformas-y-su-función)
5. [Cómo usar la plataforma](#5-cómo-usar-la-plataforma)
6. [Instalación para pruebas](#6-instalación-para-pruebas)
7. [Autor y licencia](#7-autor-y-licencia)

---

## 1. Presentación

Aplicación web para equipos de QA: organiza proyectos, suites y casos de
prueba, registra ejecuciones con su resultado, vincula defectos y mide
cobertura. Construida en Python (FastAPI) con MongoDB como única base de
datos.

### En pocas palabras

- **Qué hace:** es el cuaderno de trabajo de un equipo de QA. Ahí se definen qué
  se va a probar (casos de prueba agrupados en suites y proyectos), se anota el
  resultado de cada ejecución y se reportan los defectos encontrados.
- **Qué muestra:** cuánto está cubierto y cómo van los resultados, por proyecto
  y por suite.
- **Cómo probarlo:** entra a la [demo](https://immxew65sfxj7nubwzlszdimfi0qegzc.lambda-url.us-east-1.on.aws/),
  crea una cuenta en *Registro* y arma tu primer proyecto. Para correrlo en tu
  equipo, ve a [Instalación para pruebas](#6-instalación-para-pruebas).

Es la capa visible del proyecto insignia de QA/automatización del
portafolio. La suite de pruebas real vive en
[`pruebas-coffeemaker/`](pruebas-coffeemaker/README.md), dentro de este
mismo repositorio: JUnit, Mockito, JaCoCo, Cucumber y mutation testing
(pitest) sobre el dominio CoffeeMaker de la especialización de Coursera
"Introducción a las pruebas de software". Esas pruebas corren aparte (en
Eclipse o VS Code, no contra esta app); sus resultados se registran aquí
manualmente como Ejecuciones, con el reporte real (JaCoCo, surefire,
Cucumber, pitest) como evidencia — ver el flujo completo en el README de
esa carpeta.

### Demo en vivo

**Aplicación:** [abrir la demo en vivo](https://immxew65sfxj7nubwzlszdimfi0qegzc.lambda-url.us-east-1.on.aws/)

### Qué hace

- Registro e inicio de sesión con contraseña cifrada
- Cualquier cuenta creada desde el registro crea y edita su propio trabajo
- Proyectos, Suites de prueba y Casos de prueba, organizados jerárquicamente
- Ejecuciones de un caso con resultado (Passed / Failed / Blocked / Skipped)
- Defectos vinculados a una ejecución fallida, con severidad y estado
- Panel de cobertura y resultados por proyecto y suite

### Con qué está hecho

| Capa | Tecnología |
|---|---|
| Servidor | FastAPI, Uvicorn |
| Interfaz | Jinja2, HTMX |
| Base de datos | MongoDB |
| Sesiones | JWT en cookie httponly |
| Contraseñas | bcrypt |

---

## 2. Estructura del proyecto

```
.
├── backend/                  Aplicación web (FastAPI + MongoDB) — detalle abajo
├── pruebas-coffeemaker/      Suite de automatización QA (JUnit, Mockito,
│                             JaCoCo, Cucumber, pitest) — README propio
├── .env.example
└── README.md                 Este archivo
```

Detalle de `backend/`:

```
backend/
├── requirements.txt
└── app/
    ├── main.py              Punto de entrada, monta rutas y estáticos
    ├── config.py            Carga del .env
    ├── database.py          Conexión a Mongo e índices
    ├── seguridad.py         Hasheo de contraseñas y sesiones (JWT)
    ├── dependencias.py      Identificación del usuario y control de acceso
    ├── repositorios/        Acceso a datos por colección
    ├── routers/             Páginas web por sección
    ├── comandos/            Scripts de un solo uso (datos de ejemplo)
    ├── templates/           Plantillas Jinja2
    └── static/               Hoja de estilos y tema claro/oscuro
```

---

## 3. Arquitectura

<p align="center">
  <img src="docs/arquitectura.svg" alt="Diagrama de arquitectura: FastAPI con Mangum en AWS Lambda detrás de una Function URL, MongoDB Atlas, suite CoffeeMaker local y pruebas E2E de qa-evidencia" width="100%">
</p>

- Las páginas se generan con **Jinja2 + HTMX**; la sesión viaja en un JWT dentro
  de una cookie httponly y las contraseñas se guardan con bcrypt.
- La **suite CoffeeMaker** corre en local y sus reportes se registran en la app
  como ejecuciones.

---

## 4. Plataformas y su función

| Plataforma | Función en el proyecto |
|---|---|
| ![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white) | Ejecuta la app FastAPI mediante el adaptador Mangum, expuesta con una Function URL (sin API Gateway). |
| ![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white) | MongoDB Atlas guarda las seis colecciones: `usuarios`, `proyectos`, `suites`, `casos_prueba`, `ejecuciones` y `defectos`. No requiere ningún otro servicio ni clave de API. |
| ![qa-evidencia](https://img.shields.io/badge/qa--evidencia-2EAD33?style=for-the-badge&logo=playwright&logoColor=white) | Prueba la demo automáticamente dos veces al día y publica la evidencia. |

---

## 5. Cómo usar la plataforma

### 5.1 Crear una cuenta

1. En la página de inicio, pulsa **Crear cuenta**.
2. Completa **Nombre**, **Correo**, **Contraseña** y **Confirmar contraseña**.
3. Pulsa **Crear cuenta**. La cuenta queda lista para trabajar de inmediato.

### 5.2 Iniciar sesión

1. Pulsa **Ya tengo cuenta** (o **Ingresa** desde el registro).
2. Escribe **Correo** y **Contraseña** y pulsa **Ingresar**.
3. Entras a **Proyectos**, donde solo ves tus propios proyectos.

### 5.3 Crear un proyecto

1. En **Proyectos**, pulsa **+ Nuevo proyecto**.
2. Completa **Nombre** y **Descripción** y pulsa **Guardar**.
3. Desde la lista puedes **Editar** el proyecto o entrar con **Ver suites**.

### 5.4 Crear suites de prueba

1. Dentro del proyecto, pulsa **+ Nueva suite**.
2. Completa **Nombre** y **Descripción** y pulsa **Guardar**.
3. Cada suite ofrece **Editar**, **Ver casos** y **Eliminar**.

### 5.5 Crear casos de prueba

1. Dentro de la suite, pulsa **+ Nuevo caso**.
2. Completa el formulario:

   | Campo | Dato |
   |---|---|
   | Título | Nombre del caso |
   | Pasos (uno por línea) | Pasos a seguir, uno en cada línea |
   | Resultado esperado | Qué debe ocurrir si el sistema funciona bien |
   | Prioridad | Alta, Media o Baja |
   | Estado | Activo u Obsoleto |

3. Pulsa **Guardar**.

### 5.6 Ejecutar un caso

1. En la lista de casos, pulsa **Ejecutar**.
2. Elige el **Resultado** (Passed, Failed, Blocked o Skipped) y, si quieres,
   escribe un **Comentario**.
3. Pulsa **Registrar**. La ejecución queda en el **Historial** del caso.

### 5.7 Reportar y seguir defectos

1. Desde una ejecución, pulsa **Reportar defecto**.
2. Completa **Título**, **Descripción** (qué se esperaba, qué pasó y cómo
   reproducirlo) y **Severidad** (Crítica, Alta, Media o Baja).
3. Pulsa **Registrar defecto**.
4. En **Defectos** cambias el estado de cada uno: Abierto, En progreso o
   Cerrado.

### 5.8 Ver la cobertura

Dentro de un proyecto, **Dashboard** muestra la cobertura y los resultados por
proyecto y por suite, con acceso directo a **Ver defectos**.

---

## 6. Instalación para pruebas

Requisitos: Python 3.11+ y una base MongoDB accesible (por ejemplo, Atlas).

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate         # Linux o macOS

pip install -r requirements.txt
```

Copia `.env.example` como `.env` (en la raíz del proyecto) y completa
`MONGO_URI` y `JWT_SECRET` (genera este último con
`python -c "import secrets; print(secrets.token_urlsafe(48))"`).

```bash
cd backend
uvicorn app.main:app --reload
```

Queda en `http://127.0.0.1:8000`. Crea tu cuenta desde `/registro`.

### Despliegue

Aplicación sin estado propio en disco (todo vive en MongoDB), así que corre
igual en cualquier hospedaje con soporte para Python. La instancia pública
corre en AWS Lambda (Function URL, sin API Gateway) mediante el adaptador
`mangum`, con MongoDB Atlas como base de datos. Solo hay que definir
`MONGO_URI` y `JWT_SECRET` como variables de entorno del servicio.

---

## 7. Autor y licencia

**Luis Felipe Arias Carriazo**
[GitHub](https://github.com/lariasca1994) · [LinkedIn](https://linkedin.com/in/lfac1)

Licencia: MIT.
