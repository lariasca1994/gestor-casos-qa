# pruebas-coffeemaker

> Carpeta dentro del repositorio [`gestor-casos-qa`](../README.md) — la
> suite de automatización de ese proyecto insignia de QA. No es un
> repositorio aparte.

Portafolio de pruebas de software sobre el ejercicio **CoffeeMaker**
(especializacion Coursera "Introduccion a las pruebas de software",
Universidad de Minnesota), cubriendo las cinco tecnicas trabajadas en el
curso: JUnit, JaCoCo, Mockito, Cucumber y mutation testing (pitest).

El mismo dominio (`Recipe`, `RecipeBook`, `Inventory`, `CoffeeMaker`) se
prueba desde dos proyectos separados, cada uno con el entorno donde
realmente se ejecuta en el curso:

```
eclipse/CoffeeMaker/          JUnit + Mockito + JaCoCo   (Maven, se abre en Eclipse)
vscode/CoffeeMaker_Cucumber/  Cucumber + JaCoCo + pitest (Gradle, se abre en VS Code)
```

## Por que dos carpetas y no un solo build

Los dos ejercicios del curso usan build tools distintos (Maven en un caso,
Gradle en el otro) porque asi los entrega la propia especializacion — no
es una decision de este portafolio, es fiel a como se trabajo cada
ejercicio originalmente. Cada carpeta es un proyecto independiente y se
abre/corre por separado.

## Como ejecutar cada lado

Estas pruebas corren **en tu maquina (Eclipse o VS Code/terminal)**, no
dentro de la app web "Gestor de Casos QA". La app web es donde se
**registran los resultados** de estas ejecuciones (que suite/caso paso,
que reporte lo respalda) — no donde corren los tests. Ver la seccion
final de este README.

### Eclipse — `eclipse/CoffeeMaker`

1. `File > Import > Maven > Existing Maven Projects`, selecciona la
   carpeta `eclipse/CoffeeMaker`.
2. Para correr: click derecho sobre el proyecto > `Run As` > `Maven test`
   (usa el Maven/JDK embebido de Eclipse), o desde PowerShell parado en
   esa carpeta: `.\run-tests.ps1` (o `mvn test` directamente).
3. Reporte de cobertura: `target/site/jacoco/index.html`.

Detalle completo, incluida la tabla de que clase de test cubre que suite,
en [`eclipse/CoffeeMaker/README.md`](eclipse/CoffeeMaker/README.md).

**Verificado:** 37 tests, 0 fallos, reporte JaCoCo generado.

### VS Code — `vscode/CoffeeMaker_Cucumber`

1. Abre la carpeta `vscode/CoffeeMaker_Cucumber` en VS Code (o cualquier
   editor — no depende de una extension especifica).
2. Para correr, en PowerShell parado en esa carpeta: `.\run-tests.ps1`.
   Este script fija JDK 8 automaticamente (el wrapper de Gradle de este
   proyecto es de 2017 y no soporta Java 9+; ver el detalle en el README
   de esa carpeta si te da error de version de Java).
3. Reportes: `build/reports/tests/test/index.html` (Cucumber),
   `build/reports/jacoco/test/html/index.html` (cobertura),
   `build/reports/pitest/index.html` (mutantes).

Detalle completo en
[`vscode/CoffeeMaker_Cucumber/README.md`](vscode/CoffeeMaker_Cucumber/README.md).

**Verificado:** 10 escenarios / 30 steps, todos en verde; pitest con 238
mutaciones generadas, 116 asesinadas (49% mutation score).

## Mapeo a la matriz de casos de prueba

[`coffeemaker_test_matrix.csv`](coffeemaker_test_matrix.csv) tiene el
detalle caso por caso (7 suites, 26 casos) con la ruta exacta del reporte
que respalda cada uno. Resumen de a que proyecto pertenece cada suite:

| Suite | Tecnica | Proyecto | Ruta del reporte |
|---|---|---|---|
| `TS_RECIPE_MGMT` | JUnit | `eclipse/CoffeeMaker` | `target/surefire-reports/` |
| `TS_INVENTORY_MGMT` | JUnit | `eclipse/CoffeeMaker` | `target/surefire-reports/` |
| `TS_PURCHASE_FLOW` | JUnit | `eclipse/CoffeeMaker` | `target/surefire-reports/` |
| `TS_ROBUSTNESS_JACOCO` | JaCoCo | `eclipse/CoffeeMaker` | `target/site/jacoco/index.html` |
| `TS_MOCKITO_ISOLATION` | Mockito | `eclipse/CoffeeMaker` | `target/surefire-reports/` |
| `TS_CUCUMBER_SCENARIOS` | Cucumber | `vscode/CoffeeMaker_Cucumber` | `build/reports/tests/test/index.html` |
| `TS_JACOCO_MUTATION_CUCUMBER` | JaCoCo + pitest | `vscode/CoffeeMaker_Cucumber` | `build/reports/jacoco/test/html/index.html` + `build/reports/pitest/index.html` |

Esta tabla, junto con el CSV, es la que se usa para cargar Proyecto /
Suites / Casos en la app "Gestor de Casos QA" (carpeta [`../backend`](../backend)
de este mismo repositorio): cada ejecucion registrada ahi debe apuntar a
uno de estos reportes reales como evidencia.

## Como se conecta con el "Gestor de Casos QA"

El flujo completo de este portafolio es:

1. Corres las pruebas aca (Eclipse o VS Code/PowerShell), sobre el codigo
   real de `eclipse/CoffeeMaker` o `vscode/CoffeeMaker_Cucumber`.
2. Guardas/abres el reporte HTML que te interesa (JaCoCo, surefire,
   Cucumber, pitest).
3. En la app web "Gestor de Casos QA" registras la ejecucion del caso
   correspondiente (Passed/Failed/Blocked/Skipped) y, si aplica, el link
   o nota de que reporte la respalda.
4. El dashboard de la app muestra el panorama consolidado (cobertura por
   suite, defectos abiertos por severidad) — pero la ejecucion en si
   siempre pasa por aca, no por la web.

Si alguien revisa solo la app web sin leer este README, no va a ver forma
de "correr" las pruebas ahi — es esperado: la app es el tablero de
seguimiento, la ejecucion real vive en este repo.

## Sin datos sensibles

Ninguno de los dos proyectos se conecta a base de datos ni servicio
externo. No requieren variables de entorno ni credenciales.
