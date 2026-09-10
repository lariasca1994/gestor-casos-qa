# run-tests.ps1
# Suite JUnit + Mockito + JaCoCo (proyecto Eclipse/Maven de CoffeeMaker).
#
# Uso: abre PowerShell dentro de esta carpeta (eclipse\CoffeeMaker) y ejecuta:
#   .\run-tests.ps1
#
# No hace falta fijar un JDK especial: el pom.xml compila con Java 17 y
# Maven resuelve esto solo. Si "mvn" no se reconoce, es porque estas usando
# la terminal Git Bash integrada de Eclipse (no tiene mvn en el PATH) -
# usa una terminal de PowerShell normal, o en Eclipse: click derecho sobre
# el proyecto > Run As > Maven test.

mvn test

Write-Host ""
Write-Host "Reportes generados:" -ForegroundColor Cyan
Write-Host " - target\site\jacoco\index.html        (cobertura JaCoCo)"
Write-Host " - target\surefire-reports\              (resultado JUnit por clase, uno por suite)"
