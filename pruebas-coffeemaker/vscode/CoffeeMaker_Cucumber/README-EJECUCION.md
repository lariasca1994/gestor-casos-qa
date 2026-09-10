# CoffeeMaker Cucumber + JaCoCo

## Requisito

Ejecute el proyecto con **JDK 8**. El `build.gradle` original valida esta versión.

## Eclipse

1. Descomprima el archivo ZIP.
2. En Eclipse, seleccione **File > Import > Gradle > Existing Gradle Project**.
3. Seleccione la carpeta `CoffeeMaker_Cucumber`.
4. Configure Eclipse para usar JDK 8: **Window > Preferences > Java > Installed JREs**.
5. En la vista Gradle Tasks ejecute `verification > test` o `verification > check`.

## Consola de Windows

```bat
gradlew.bat clean test jacocoTestReport
```

El informe HTML queda en:

```
build\reports\jacoco\test\html\index.html
```

El informe XML queda en:

```
build\reports\jacoco\test\jacocoTestReport.xml
```

Las pruebas Cucumber están en `src/test/resources/.../CoffeeMaker.feature` y las definiciones de pasos están en `src/test/java/.../TestSteps.java`.
