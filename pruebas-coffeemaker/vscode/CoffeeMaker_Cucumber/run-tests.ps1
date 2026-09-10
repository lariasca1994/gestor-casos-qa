# run-tests.ps1
# Suite Cucumber + JaCoCo + pitest (mutation testing) del proyecto
# CoffeeMaker_Cucumber, via Gradle.
#
# Uso: abre PowerShell dentro de esta carpeta (vscode\CoffeeMaker_Cucumber)
# y ejecuta:
#   .\run-tests.ps1
#
# Por que existe este script: el wrapper de Gradle de este proyecto es
# viejo (4.3.1) y no sabe interpretar el formato de version de Java 9+.
# Si tu Java por defecto es mas nuevo (ej. 21), gradlew.bat falla con
# "Could not determine java version from '21.x.x'" antes de llegar a
# compilar nada. Este script fija JDK 8 SOLO para esta ejecucion, sin
# tocar tu Java por defecto (Eclipse y otros proyectos siguen usando el
# que ya tengas configurado).
#
# Si tu JDK 8 esta instalado en otra ruta, cambia la siguiente linea:
$jdk8 = "C:\Program Files\Eclipse Adoptium\jdk-8.0.502.7-hotspot"

if (-not (Test-Path $jdk8)) {
    Write-Host "No se encontro un JDK 8 en: $jdk8" -ForegroundColor Red
    Write-Host "Edita la variable `$jdk8 al inicio de este script con la ruta correcta," -ForegroundColor Red
    Write-Host "o instala Eclipse Temurin 8 desde https://adoptium.net/temurin/releases/?version=8" -ForegroundColor Red
    exit 1
}

$env:JAVA_HOME = $jdk8
$env:Path = "$env:JAVA_HOME\bin;$env:Path"

Write-Host "Usando JDK 8 en: $jdk8"

& .\gradlew.bat clean test jacocoTestReport pitest

Write-Host ""
Write-Host "Reportes generados:" -ForegroundColor Cyan
Write-Host " - build\reports\tests\test\index.html         (JUnit/Cucumber - escenarios y steps)"
Write-Host " - build\reports\jacoco\test\html\index.html   (cobertura JaCoCo)"
Write-Host " - build\reports\pitest\index.html             (mutation testing - pitest)"
