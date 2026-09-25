# Gestor de Casos de Prueba QA

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-3D72D7?style=flat&logo=htmx&logoColor=white)
![Jinja](https://img.shields.io/badge/Jinja2-B41717?style=flat&logo=jinja&logoColor=white)

Aplicación web para equipos de QA: organiza proyectos, suites y casos de
prueba, registra ejecuciones con su resultado, vincula defectos y mide
cobertura. Construida en Python (FastAPI) con MongoDB como única base de
datos.

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

## Demo en vivo

**Aplicación:** [immxew65sfxj7nubwzlszdimfi0qegzc.lambda-url.us-east-1.on.aws](https://immxew65sfxj7nubwzlszdimfi0qegzc.lambda-url.us-east-1.on.aws/)

## Qué hace

- Registro e inicio de sesión con contraseña cifrada
- Roles QA: cualquier cuenta QA crea y edita
- Proyectos, Suites de prueba y Casos de prueba, organizados jerárquicamente
- Ejecuciones de un caso con resultado (Passed / Failed / Blocked / Skipped)
- Defectos vinculados a una ejecución fallida, con severidad y estado
- Panel de cobertura y resultados por proyecto y suite

## Con qué está hecho

| Capa | Tecnología |
|---|---|
| Servidor | FastAPI, Uvicorn |
| Interfaz | Jinja2, HTMX |
| Base de datos | MongoDB |
| Sesiones | JWT en cookie httponly |
| Contraseñas | bcrypt |

## Estructura

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
    ├── dependencias.py      Identificación del usuario, exige login/rol
    ├── repositorios/        Acceso a datos por colección
    ├── routers/             Páginas web por sección
    ├── comandos/            Scripts de un solo uso (crear cuenta ADMIN)
    ├── templates/           Plantillas Jinja2
    └── static/               Hoja de estilos y tema claro/oscuro
```

## Diagrama de Arquitectura

```mermaid
flowchart TB
    %% ============================================================
    %%  DIAGRAMA DE ARQUITECTURA — GESTOR DE CASOS QA
    %%  Colores basados en las guías de marca oficiales de cada tecnología.
    %% ============================================================

    subgraph Usuario["👤 Usuario QA"]
        Browser["Navegador Web<br/>Jinja2 + HTMX"]
    end

    subgraph AWS["☁️ AWS Lambda"]
        subgraph App["Aplicación FastAPI"]
            Mangum["Mangum<br/>Adaptador ASGI"]
            Main["main.py<br/>Punto de entrada"]
            Routers["routers/<br/>Páginas por sección"]
            Templates["templates/<br/>Plantillas Jinja2"]
            Static["static/<br/>CSS · Tema claro/oscuro"]
        end

        subgraph Seguridad["Autenticación"]
            JWT["JWT<br/>Cookie httponly"]
            Bcrypt["bcrypt<br/>Hash de contraseñas"]
        end

        subgraph Datos["Acceso a datos"]
            Repos["repositorios/<br/>Por colección"]
            Database["database.py<br/>Conexión Mongo + índices"]
        end
    end

    subgraph MongoDB["🗄️ MongoDB Atlas"]
        Colecciones["Colecciones:<br/>usuarios · proyectos · suites<br/>casos_prueba · ejecuciones · defectos"]
    end

    subgraph Pruebas["🧪 Suite de pruebas (repo aparte)"]
        JUnit["JUnit + Mockito"]
        JaCoCo["JaCoCo"]
        Cucumber["Cucumber"]
        Pitest["pitest"]
    end

    %% ---- Flujo de datos ----
    Browser -->|HTTPS| Mangum
    Mangum --> Main
    Main --> Routers
    Routers --> Templates
    Routers --> Static
    Routers --> JWT
    JWT --> Bcrypt
    Routers --> Repos
    Repos --> Database
    Database -->|PyMongo| Colecciones
    Pruebas -.->|Resultados registrados<br/>manualmente| Browser

    %% ---- Colores de marca (Brand Colors) ----
    classDef fastapi fill:#009688,stroke:#004D40,stroke-width:2px,color:#FFFFFF;
    classDef mongodb fill:#47A248,stroke:#1B5E20,stroke-width:2px,color:#FFFFFF;
    classDef jinja fill:#B41717,stroke:#7F0000,stroke-width:2px,color:#FFFFFF;
    classDef htmx fill:#3D72D7,stroke:#1A3A6C,stroke-width:2px,color:#FFFFFF;
    classDef aws fill:#FF9900,stroke:#B36B00,stroke-width:2px,color:#000000;
    classDef python fill:#3572A5,stroke:#1A3A5C,stroke-width:2px,color:#FFFFFF;
    classDef security fill:#333333,stroke:#000000,stroke-width:2px,color:#FFFFFF;
    classDef neutral fill:#F5F5F5,stroke:#CCCCCC,stroke-width:1px,color:#333333;
    classDef test fill:#F3E8FF,stroke:#8A05FF,stroke-width:1px,color:#333333;

    class Browser neutral;
    class Mangum,Main,Routers,Templates,Static fastapi;
    class Repos,Database python;
    class Colecciones mongodb;
    class JWT,Bcrypt security;
    class JUnit,JaCoCo,Cucumber,Pitest test;

    %% ---- Estilos de subgráficos ----
    style Usuario fill:#FAFAFA,stroke:#DDDDDD,stroke-width:1px;
    style AWS fill:#FFF8E1,stroke:#FF9900,stroke-width:2px,stroke-dasharray:5 5;
    style App fill:#E0F2F1,stroke:#009688,stroke-width:1px;
    style Seguridad fill:#F5F5F5,stroke:#333333,stroke-width:1px;
    style Datos fill:#E3F2FD,stroke:#3572A5,stroke-width:1px;
    style MongoDB fill:#E8F5E9,stroke:#47A248,stroke-width:2px,stroke-dasharray:5 5;
    style Pruebas fill:#F3E8FF,stroke:#8A05FF,stroke-width:1px,stroke-dasharray:3 3;
```

## A qué se conecta

Una única base MongoDB con estas colecciones: `usuarios`, `proyectos`,
`suites`, `casos_prueba`, `ejecuciones`, `defectos`. No requiere ningún otro
servicio ni clave de API.

## Cómo ejecutarlo

Requisitos: Python 3.11+ y una base MongoDB accesible (Atlas M0 gratis
alcanza de sobra).

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

Queda en `http://127.0.0.1:8000`.

Las cuentas creadas desde `/registro` quedan con rol QA.

## Despliegue

Aplicación sin estado propio en disco (todo vive en MongoDB), así que corre
igual en cualquier hospedaje con soporte para Python. La instancia pública
corre en AWS Lambda (Function URL, sin API Gateway) mediante el adaptador
`mangum`, con MongoDB Atlas M0 como base de datos. Solo hay que definir
`MONGO_URI` y `JWT_SECRET` como variables de entorno del servicio.

## Autor

**Luis Felipe Arias Carriazo**
[GitHub](https://github.com/lariasca1994) · [LinkedIn](https://linkedin.com/in/lfac1)