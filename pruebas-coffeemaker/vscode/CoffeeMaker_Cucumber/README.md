# CoffeeMaker_Cucumber — Cucumber + JaCoCo + pitest (mutation testing)

Proyecto Gradle sobre el mismo ejercicio **CoffeeMaker** (Coursera —
Universidad de Minnesota), enfocado en dos tecnicas que no viven en el
lado Eclipse/Maven: pruebas de aceptacion en Gherkin/Cucumber, y mutation
testing con pitest sobre esas mismas pruebas.

- **Cucumber** — escenarios en `CoffeeMaker.feature` (Gherkin), ejecutados
  via JUnit runner (`RunCukesTest`) contra el `TestSteps` de este proyecto.
- **JaCoCo** — cobertura de la ejecucion de los escenarios.
- **pitest** — mutation testing: genera mutantes del codigo de dominio y
  verifica cuantos "mata" la suite de Cucumber (si un mutante sobrevive,
  significa que las pruebas no detectarian ese cambio de comportamiento).

**Verificado:** 10 escenarios / 30 steps, todos en verde. Build de pitest
exitoso: 238 mutaciones generadas, 116 asesinadas (**49% mutation
score**) — desglose por mutator disponible en el reporte HTML.

## Como correrlo

Requiere JDK 8 para el wrapper de Gradle (version 4.3.1, no soporta
Java 9+) — ver la nota abajo si tu JDK por defecto es mas nuevo.

**Opcion A — script (recomendado)**, parado en esta carpeta:

```
.\run-tests.ps1
```

Este script fija JDK 8 solo para esta ejecucion (sin tocar tu Java por
defecto en el resto del sistema/Eclipse) y corre Gradle con las tres
tareas necesarias.

**Opcion B — manual**, en PowerShell:

```
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-8.0.502.7-hotspot"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
.\gradlew.bat clean test jacocoTestReport pitest
```

(Ajusta la ruta del JDK 8 si en tu maquina esta instalado en otro lugar.)

### Por que hace falta fijar JDK 8

El wrapper (`gradle/wrapper/gradle-wrapper.properties`) apunta a Gradle
4.3.1, que no sabe interpretar el formato de version de Java 9 en
adelante ("21.0.12"). Sin importar lo que digas en `gradle.properties`
(`org.gradle.java.home`), el propio `gradlew.bat` necesita arrancar con
un JDK compatible desde el principio — por eso `JAVA_HOME` se fija en la
terminal antes de invocar el wrapper, no solo en `gradle.properties`.

### Reportes generados

```
build/reports/tests/test/index.html         Cucumber/JUnit — 10 escenarios, 30 steps
build/reports/jacoco/test/html/index.html    Cobertura JaCoCo
build/reports/pitest/index.html              Mutation testing — detalle por mutator y clase
```

## Nota sobre `Cucumber-RE-initial`

Este repo tuvo originalmente una segunda carpeta, `Cucumber-RE-initial`,
que se descarto del portafolio: su `build.gradle` nunca paso de la
plantilla por defecto de `gradle init`, y su suite de pruebas
(`skeleton/TestSteps.java`) depende de una clase `UICmd.java` que no
existe en ningun lugar del proyecto original — es un ejercicio distinto
que quedo sin terminar, no parte de este trabajo de pruebas.

## Sin datos sensibles

Este proyecto no se conecta a ninguna base de datos ni servicio externo.
No requiere variables de entorno ni credenciales.
