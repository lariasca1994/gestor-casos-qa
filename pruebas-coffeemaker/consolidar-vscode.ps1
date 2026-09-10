# Arma A:\Github\pruebas-coffeemaker\vscode a partir de lo que ya esta en
# A:\Coursera. CoffeeMaker_Cucumber se toma de "entrega-jacoco" porque es
# la copia con el build.gradle correcto (JaCoCo configurado) y el codigo
# mas reciente. Se excluyen las cachés/salidas de build (.gradle, build,
# .settings) y los archivos de proyecto de Eclipse (.project, .classpath)
# para que el repo quede limpio.

$repo = "A:\Github\pruebas-coffeemaker\vscode"
New-Item -ItemType Directory -Force -Path $repo | Out-Null

robocopy "A:\Coursera\entrega-jacoco\CoffeeMaker_Cucumber" "$repo\CoffeeMaker_Cucumber" /E /XD .gradle build .settings /XF .project .classpath

robocopy "A:\Coursera\Cucumber-RE-initial" "$repo\Cucumber-RE-initial" /E /XD .gradle build

Write-Host "Listo. Robocopy termina con codigo 1 o 3 en un copiado normal (no es error)."
