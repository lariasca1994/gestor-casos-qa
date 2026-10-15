# 📘 Manual de usuario · Gestor de Casos de Prueba QA

Guía para usar la plataforma paso a paso: qué significa cada campo, qué datos se ingresan y qué
protege la plataforma. Para la parte técnica vuelve al [README](../README.md).

**Demo:** [Gestor QA (AWS Lambda)](https://immxew65sfxj7nubwzlszdimfi0qegzc.lambda-url.us-east-1.on.aws/)

## Contenido

1. [En pocas palabras](#1-en-pocas-palabras)
2. [Antes de empezar](#2-antes-de-empezar)
3. [Paso a paso](#3-paso-a-paso)
4. [Qué información ingresas y dónde queda](#4-qué-información-ingresas-y-dónde-queda)
5. [Seguridad: qué se garantiza](#5-seguridad-qué-se-garantiza)
6. [Límites y recomendaciones](#6-límites-y-recomendaciones)
7. [Preguntas frecuentes](#7-preguntas-frecuentes)

---

## 1. En pocas palabras

Es el cuaderno de trabajo de un equipo de QA. El trabajo se organiza así:

```
Proyecto → Suites de prueba → Casos de prueba → Ejecuciones → Defectos
```

Defines qué vas a probar, anotas el resultado de cada ejecución, reportas los defectos y ves la
cobertura en un tablero.

## 2. Antes de empezar

- Solo necesitas un navegador.
- Al crear tu cuenta, la plataforma te agrega **proyectos de ejemplo** con suites y casos ya
  escritos, para que veas cómo se usa desde el primer momento.

## 3. Paso a paso

### 3.1 Crear una cuenta

![Formulario de registro con sus campos numerados](img/manual/01-registro.png)

| # | Campo | Qué escribir | Reglas |
|:-:|---|---|---|
| 1 | Nombre | Tu nombre; aparece arriba a la derecha | Obligatorio |
| 2 | Correo | El correo con el que vas a entrar | Formato válido y único |
| 3 | Contraseña | Tu contraseña | Mínimo **8 caracteres** |
| 4 | Confirmar contraseña | La misma contraseña | Debe coincidir con el campo 3 |
| 5 | Crear cuenta | Botón | Crea la cuenta con rol **QA** y te deja con la sesión iniciada |

El registro siempre crea cuentas con rol QA. El rol de administrador no se puede pedir desde el
formulario.

### 3.2 Iniciar sesión

![Formulario de inicio de sesión](img/manual/02-login.png)

| # | Campo | Qué escribir |
|:-:|---|---|
| 1 | Correo | El correo de tu cuenta |
| 2 | Contraseña | Tu contraseña |
| 3 | Ingresar | Abre tu lista de proyectos |

Si el correo o la contraseña no coinciden, el mensaje es el mismo en ambos casos.

### 3.3 Proyectos

![Lista de proyectos](img/manual/03-proyectos.png)

| # | Elemento | Qué hace |
|:-:|---|---|
| 1 | + Nuevo proyecto | Abre el formulario para crear un proyecto |
| 2 | Ver suites | Entra al proyecto |
| 3 | Editar | Cambia el nombre o la descripción |

Solo ves **tus** proyectos. El administrador ve todos.

### 3.4 Crear un proyecto

![Formulario de proyecto](img/manual/04-proyecto-nuevo.png)

| # | Campo | Qué escribir | Reglas |
|:-:|---|---|---|
| 1 | Nombre | Nombre del sistema o producto que vas a probar | Obligatorio |
| 2 | Descripción | Alcance de las pruebas | Opcional |
| 3 | Guardar | Botón | Crea el proyecto |

### 3.5 Suites de prueba

![Suites de un proyecto](img/manual/05-suites.png)

Una suite agrupa casos de un mismo módulo o tipo de prueba.

| # | Elemento | Qué hace |
|:-:|---|---|
| 1 | + Nueva suite | Crea una suite con **Nombre** (obligatorio) y **Descripción** |
| 2 | Ver casos | Entra a los casos de la suite |

Cada suite también ofrece **Editar** y **Eliminar**.

### 3.6 Casos de prueba

![Casos de una suite](img/manual/06-casos.png)

| # | Elemento | Qué hace |
|:-:|---|---|
| 1 | + Nuevo caso | Abre el formulario del caso |
| 2 | Ejecutar | Registra el resultado de una ejecución |

La columna **Último resultado** muestra cómo terminó la ejecución más reciente.

### 3.7 Crear un caso

![Formulario de caso de prueba con sus campos numerados](img/manual/07-caso-nuevo.png)

| # | Campo | Qué escribir | Reglas |
|:-:|---|---|---|
| 1 | Título | Qué valida el caso, en una frase | Obligatorio |
| 2 | Pasos | Las acciones a seguir, **una por línea** | Cada línea se guarda como un paso numerado |
| 3 | Resultado esperado | Qué debe ocurrir si el sistema funciona bien | — |
| 4 | Prioridad | Alta, Media o Baja | Por defecto, Media |
| 5 | Estado | Activo u Obsoleto | Los obsoletos se conservan como historial |
| 6 | Guardar | Botón | Crea el caso |

### 3.8 Ejecutar un caso

![Registro de una ejecución e historial](img/manual/08-ejecuciones.png)

| # | Campo | Qué escribir |
|:-:|---|---|
| 1 | Resultado | **Passed** (pasó), **Failed** (falló), **Blocked** (no se pudo ejecutar) o **Skipped** (se omitió) |
| 2 | Comentario | Opcional: qué observaste |
| 3 | Registrar | Guarda la ejecución en el **Historial** |
| 4 | Reportar defecto | Aparece en las ejecuciones fallidas para registrar el defecto encontrado |

### 3.9 Reportar un defecto

![Formulario de defecto](img/manual/09-defecto-nuevo.png)

| # | Campo | Qué escribir |
|:-:|---|---|
| 1 | Título | Resumen del problema |
| 2 | Descripción | Qué se esperaba, qué pasó y cómo reproducirlo |
| 3 | Severidad | Crítica, Alta, Media o Baja |
| 4 | Registrar defecto | Botón |

### 3.10 Seguimiento de defectos

![Lista de defectos del proyecto](img/manual/10-defectos.png)

En **Defectos** cambias el estado de cada uno: **Abierto**, **En progreso** o **Cerrado**.

### 3.11 Dashboard de cobertura

![Dashboard de cobertura y resultados](img/manual/11-dashboard.png)

| Bloque | Qué muestra |
|---|---|
| Cobertura de ejecución | Porcentaje de casos ejecutados al menos una vez |
| Resultados | Cuántos casos terminaron en Passed, Failed, Blocked o Skipped en su última ejecución, y cuántos siguen sin ejecutar |
| Cobertura por suite | El mismo detalle, suite por suite |
| Defectos abiertos por severidad | Cuántos defectos siguen abiertos de cada severidad |

## 4. Qué información ingresas y dónde queda

| Dato | Para qué se usa | Dónde se guarda | Quién lo ve |
|---|---|---|---|
| Nombre y correo | Identificar tu cuenta | MongoDB Atlas | Tú y el administrador |
| Contraseña | Iniciar sesión | MongoDB Atlas, **solo su huella bcrypt** | Nadie: no se puede leer ni recuperar |
| Proyectos, suites, casos, ejecuciones y defectos | Tu trabajo de QA | MongoDB Atlas, marcados con tu cuenta | Tú y el administrador |
| Sesión | Mantenerte conectado | Cookie en tu navegador | Firmada, invisible para JavaScript, vence a las 8 horas |

## 5. Seguridad: qué se garantiza

Comprobado en el código del proyecto (`backend/app/seguridad.py`, `dependencias.py`,
`routers/web_auth.py`):

- **Contraseñas con bcrypt** (12 rondas). Solo se guarda la huella.
- **Sesión con JWT en cookie `HttpOnly` y `SameSite=Lax`**, firmada con una clave secreta del
  servidor y válida por 8 horas. **Salir** la borra.
- **Control de acceso por dueño:** cada proyecto, con todo lo que contiene, solo lo puede ver o
  editar quien lo creó o un administrador. Cambiar el identificador en la URL no da acceso a
  proyectos ajenos.
- **Roles separados:** el registro solo crea cuentas QA; el administrador se crea aparte, por
  comando, nunca desde un formulario. Solo el administrador puede archivar o eliminar proyectos y
  suspender cuentas.
- **Suspensión inmediata:** en cada petición se revisa que la cuenta siga activa; una cuenta
  suspendida queda fuera sin esperar a que venza su sesión.
- **Mensaje de error genérico** al iniciar sesión, para no revelar qué correos existen.
- **Plantillas con escape automático** (Jinja2): lo que escribes se muestra como texto, no como
  código.
- **Secretos fuera del repositorio:** la conexión a MongoDB y la clave JWT viven en variables de
  entorno de AWS Lambda.

## 6. Límites y recomendaciones

Es una demo de portafolio:

- No hay bloqueo por intentos fallidos ni recuperación de contraseña por correo.
- La contraseña solo exige 8 caracteres: usa una frase larga que no uses en otros sitios.
- No escribas datos personales o confidenciales en los casos y defectos.

## 7. Preguntas frecuentes

**¿De dónde salieron los proyectos que veo al entrar?** Son los proyectos de ejemplo que la
plataforma crea al registrarte. Puedes editarlos o usarlos como plantilla.

**¿Puedo borrar un proyecto?** Archivar y eliminar proyectos es una acción reservada al
administrador, para no perder historial de pruebas por error.

**¿Qué diferencia hay entre Blocked y Skipped?** *Blocked*: el caso no se pudo ejecutar por un
impedimento (ambiente caído, dato faltante). *Skipped*: se decidió no ejecutarlo en esa ronda.

**¿Qué significa la pantalla "Estamos en mantenimiento"?** El servicio o su base de datos no están respondiendo en ese momento. No se perdió nada: tus proyectos, suites, casos y defectos siguen guardados, y ninguna acción quedó a medias (si no viste la confirmación, no se guardó). La pantalla se actualiza sola y vuelve a la normalidad apenas el servicio responda; también puedes reintentar más tarde.
