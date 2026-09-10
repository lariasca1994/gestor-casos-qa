---
title: Datos para cargar en Gestor de Casos QA — Proyecto CoffeeMaker
---

# Carga en Gestor de Casos QA — Proyecto CoffeeMaker

Referencia lista para copiar/pegar en los formularios de la app. Sigue el
orden: primero el Proyecto, luego cada Suite (con su descripción, que
incluye dónde vive el reporte real), y dentro de cada Suite sus Casos.

La app solo admite tres niveles de prioridad (Alta / Media / Baja). Donde
la matriz original decía "P0 - Crítica" lo mapeo a **Alta** (no hay nivel
separado para crítica); "P1 - Alta" → Alta; "P2 - Media" → Media. Lo
indico entre paréntesis en cada caso para que lo veas.

Los "Pasos" van uno por línea en el textarea de la app (no hace falta
escribir el número, la app no los numera — los dejo numerados aquí solo
para que los copies en orden).

---

## Proyecto

- **Nombre**: CoffeeMaker
- **Descripción**: Portafolio de pruebas del ejercicio CoffeeMaker (Coursera — Universidad de Minnesota). Ejecución en escritorio: eclipse/CoffeeMaker (JUnit+Mockito+JaCoCo) y vscode/CoffeeMaker_Cucumber (Cucumber+JaCoCo+pitest). Ver README del repo pruebas-coffeemaker para correrlas.

---

## Suite 1 — JUnit — Gestión de Recetas

- **Nombre**: JUnit — Gestión de Recetas
- **Descripción**: Origen: eclipse/CoffeeMaker. Reporte: target/surefire-reports/ (tras `mvn test` o `.\run-tests.ps1`).

**TC-REC-001 — Creación exitosa de una receta válida**
Pasos:
1. Acceder al módulo de administración de recetas.
2. Ingresar nombre 'Capuchino'.
3. Especificar precio 50.
4. Definir ingredientes: café 2, leche 3, azúcar 1, chocolate 0.
5. Confirmar guardado.
Resultado esperado: La receta se registra en el catálogo, el sistema retorna confirmación de éxito y queda disponible para compra.
Prioridad: Alta (P1)

**TC-REC-002 — Rechazo de receta duplicada por nombre**
Pasos:
1. Registrar receta 'Latte'.
2. Intentar registrar una segunda receta con nombre 'Latte'.
3. Enviar solicitud de guardado.
Resultado esperado: El sistema rechaza la operación, genera error por duplicado y mantiene una sola instancia.
Prioridad: Media (P2)

**TC-REC-003 — Control de límite máximo de recetas**
Pasos:
1. Cargar recetas hasta alcanzar la capacidad máxima (3 o 4 recetas).
2. Intentar agregar una nueva receta válida.
Resultado esperado: El sistema bloquea la adición indicando catálogo lleno; no sobreescribe ninguna receta existente.
Prioridad: Media (P2)

**TC-REC-004 — Validación de valores numéricos negativos o nulos**
Pasos:
1. Iniciar registro de receta.
2. Asignar precio negativo (-10) o cantidad de café negativa (-2).
3. Confirmar operación.
Resultado esperado: Error de validación previo a persistencia; la receta no se agrega y el sistema exige enteros positivos/cero válidos.
Prioridad: Alta (P1)

---

## Suite 2 — JUnit — Gestión de Inventario

- **Nombre**: JUnit — Gestión de Inventario
- **Descripción**: Origen: eclipse/CoffeeMaker. Reporte: target/surefire-reports/ (tras `mvn test` o `.\run-tests.ps1`).

**TC-INV-001 — Reabastecimiento exitoso de inventario**
Pasos:
1. Consultar estado actual (15 de cada uno).
2. Ejecutar acción de añadir suministros: café +5, leche +10, azúcar +5, chocolate +2.
3. Confirmar operación.
Resultado esperado: El stock se actualiza aditivamente a los valores acumulados correctos (café 20, leche 25, azúcar 20, chocolate 17).
Prioridad: Alta (P1)

**TC-INV-002 — Rechazo de suministros con valores negativos o no numéricos**
Pasos:
1. Intentar agregar unidades negativas (leche -5) o caracteres alfanuméricos.
2. Solicitar actualización de inventario.
Resultado esperado: Se rechaza la transacción por argumento inválido; los niveles de inventario permanecen intactos.
Prioridad: Media (P2)

---

## Suite 3 — JUnit — Flujo de Compra y Transacciones

- **Nombre**: JUnit — Flujo de Compra y Transacciones
- **Descripción**: Origen: eclipse/CoffeeMaker. Reporte: target/surefire-reports/ (tras `mvn test` o `.\run-tests.ps1`).

**TC-PUR-001 — Compra exitosa con dinero exacto y stock suficiente**
Pasos:
1. Verificar receta 'Espresso' con costo 35 y stock suficiente.
2. Seleccionar 'Espresso'.
3. Ingresar importe 35.
4. Ejecutar orden de compra.
Resultado esperado: Se despacha bebida, cambio devuelto es 0, y se descuentan los ingredientes de forma atómica.
Prioridad: Alta (P0 - Crítica → Alta)

**TC-PUR-002 — Compra exitosa con excedente de pago (Cálculo de cambio)**
Pasos:
1. Seleccionar receta con costo 50.
2. Ingresar monto de pago 100.
3. Confirmar compra.
Resultado esperado: Se despacha bebida, retorna cambio de 50 y se descuentan los ingredientes correctamente.
Prioridad: Alta (P0 → Alta)

**TC-PUR-003 — Rechazo por fondos insuficientes**
Pasos:
1. Seleccionar receta con costo 50.
2. Ingresar únicamente 30.
3. Confirmar compra.
Resultado esperado: No se despacha bebida, el sistema retorna la totalidad del dinero ingresado (30) y el inventario no se modifica.
Prioridad: Alta (P1)

**TC-PUR-004 — Rechazo por stock insuficiente (Ingredientes agotados)**
Pasos:
1. Ajustar inventario para que leche sea 0.
2. Seleccionar receta que requiera leche (costo 40).
3. Ingresar 50.
4. Proceder con la compra.
Resultado esperado: Dispensado cancelado por falta de insumos, devolución íntegra del dinero (50) e inventario inalterado.
Prioridad: Alta (P1)

---

## Suite 4 — JaCoCo — Cobertura Estructural por Clase

- **Nombre**: JaCoCo — Cobertura Estructural por Clase
- **Descripción**: Origen: eclipse/CoffeeMaker. Reporte: target/site/jacoco/index.html (tras `mvn test` o `.\run-tests.ps1`).

**TC-COV-001 — Cobertura estructural de la clase CoffeeMaker**
Pasos:
1. Ejecutar build con agente JaCoCo ('mvn clean test').
2. El reporte se genera en el mismo build (no hace falta 'mvn jacoco:report' aparte).
3. Inspeccionar métricas de Line Coverage e Instruction Coverage para CoffeeMaker.java.
Resultado esperado: Line Coverage e Instruction Coverage >= 90% y cobertura de branches >= 85%.
Prioridad: Alta (P0 → Alta)

**TC-COV-002 — Cobertura estructural de la clase RecipeBook**
Pasos:
1. Ejecutar suite de pruebas unitarias sobre RecipeBook.
2. Verificar métricas en el reporte HTML de JaCoCo.
Resultado esperado: Line Coverage = 100% (incluyendo flujos de slots vacíos, reemplazos y adición).
Prioridad: Alta (P1)

**TC-COV-003 — Cobertura estructural de la clase Inventory**
Pasos:
1. Ejecutar pruebas sobre operaciones de inventario.
2. Inspeccionar cobertura de decisiones en Inventory.java.
Resultado esperado: Branch Coverage = 100% en enoughIngredients() y useIngredients(), Line Coverage >= 95%.
Prioridad: Alta (P0 → Alta)

**TC-COV-004 — Cobertura estructural de la clase Recipe**
Pasos:
1. Ejecutar pruebas unitarias de getters, setters, parseo y método equals().
2. Consultar reporte JaCoCo para la entidad Recipe.
Resultado esperado: Line Coverage y Method Coverage = 100%, cubriendo todas las ramas de RecipeException.
Prioridad: Media (P2)

---

## Suite 5 — Mockito — Pruebas Unitarias Aisladas

- **Nombre**: Mockito — Pruebas Unitarias Aisladas
- **Descripción**: Origen: eclipse/CoffeeMaker. Reporte: target/surefire-reports/ (clase CoffeeMakerMockitoTest, mismo build de `mvn test`).

**TC-MCK-001 — CoffeeMaker usa RecipeBook mockeado al listar recetas**
Pasos:
1. Mockear RecipeBook (@Mock).
2. Inyectar mock en CoffeeMaker.
3. Configurar when(recipeBookMock.getRecipes()).thenReturn(stubArray).
4. Invocar coffeeMaker.getRecipes().
Resultado esperado: coffeeMaker.getRecipes() retorna el arreglo simulado y se comprueba verify(recipeBookMock, times(1)).getRecipes().
Prioridad: Alta (P1)

**TC-MCK-002 — CoffeeMaker delega consumo en Inventory mockeado al procesar compra**
Pasos:
1. Mockear Inventory.
2. Configurar when(inventoryMock.useIngredients(any())).thenReturn(true).
3. Ejecutar coffeeMaker.makeCoffee(index, amtPaid).
Resultado esperado: Se verifica verify(inventoryMock).useIngredients(expectedRecipe) únicamente si el monto de pago es suficiente.
Prioridad: Alta (P0 → Alta)

**TC-MCK-003 — CoffeeMaker maneja rechazo controlado de persistencia en RecipeBook mockeado**
Pasos:
1. Mockear RecipeBook.
2. Configurar when(recipeBookMock.addRecipe(any())).thenReturn(false).
3. Invocar coffeeMaker.addRecipe(recipe).
Resultado esperado: CoffeeMaker propaga o maneja coherentemente el valor booleano false sin corromper su estado interno.
Prioridad: Media (P2)

---

## Suite 6 — Cucumber — Escenarios BDD Agrupados

- **Nombre**: Cucumber — Escenarios BDD Agrupados
- **Descripción**: Origen: vscode/CoffeeMaker_Cucumber. Reporte: build/reports/tests/test/index.html (tras `.\run-tests.ps1` o `gradlew.bat clean test`). Un solo CoffeeMaker.feature, corre todos los escenarios en un build.

**TC-CUC-001 — Grupo: Identidad, Ciclo de Vida y Restricciones de Recetas**
Pasos:
1. Ejecutar 'gradlew.bat clean test' (o `.\run-tests.ps1`) sobre CoffeeMaker_Cucumber.
2. En build/reports/tests/test/index.html, revisar los escenarios de creación, unicidad por nombre, edición, eliminación y límite máximo de recetas.
Resultado esperado: Todos los pasos Gherkin (Given-When-Then) pasan en verde (100% aprobación en catálogo).
Prioridad: Alta (P1)

**TC-CUC-002 — Grupo: Flujo de Compra y Manejo de Dinero**
Pasos:
1. Ejecutar 'gradlew.bat clean test' (o `.\run-tests.ps1`) sobre CoffeeMaker_Cucumber.
2. En build/reports/tests/test/index.html, revisar los escenarios (incluidas las tablas Scenario Outline) sobre pago exacto, cálculo de cambio y rechazo por dinero insuficiente.
Resultado esperado: Se ejecutan todas las combinaciones de la tabla; despacho conforme y cálculo matemático de vueltas verificado.
Prioridad: Alta (P0 → Alta)

**TC-CUC-003 — Grupo: Abastecimiento y Consumo Crítico de Inventario**
Pasos:
1. Ejecutar 'gradlew.bat clean test' (o `.\run-tests.ps1`) sobre CoffeeMaker_Cucumber.
2. En build/reports/tests/test/index.html, revisar los escenarios sobre incremento de stock, consumo tras compra y bloqueo por falta de suministros.
Resultado esperado: Bloqueo efectivo de transacciones ante faltante de stock; inventario inalterado tras transacciones fallidas.
Prioridad: Alta (P1)

**TC-CUC-004 — Grupo: Robustez de Entrada y Fronteras de Usuario**
Pasos:
1. Ejecutar 'gradlew.bat clean test' (o `.\run-tests.ps1`) sobre CoffeeMaker_Cucumber.
2. En build/reports/tests/test/index.html, revisar los escenarios que envían cadenas alfanuméricas en campos numéricos y valores negativos.
Resultado esperado: Captura limpia de excepciones sin interrupción abrupta del sistema ni corrupción de datos.
Prioridad: Media (P2)

---

## Suite 7 — JaCoCo + Mutantes (Cucumber)

- **Nombre**: JaCoCo + Mutantes (Cucumber)
- **Descripción**: Origen: vscode/CoffeeMaker_Cucumber. Reporte: build/reports/jacoco/test/html/index.html + build/reports/pitest/index.html (tras `.\run-tests.ps1`, que ya corre jacocoTestReport y pitest).

**TC-MUT-001 — Cobertura BDD Global de Clases de Dominio (JaCoCo)**
Pasos:
1. Ejecutar suite de Cucumber con agente JaCoCo activo.
2. Generar reporte consolidado HTML.
Resultado esperado: Cobertura de código de pruebas BDD >= 88% sobre el paquete edu.ncsu.csc326.coffeemaker.
Prioridad: Alta (P0 → Alta)

**TC-MUT-002 — Eliminación de Mutante M1 — Operadores Relacionales e Inversión Condicional**
Pasos:
1. Configurar PITest con Conditionals Boundary Mutator / Invert Negatives Mutator.
2. Ejecutar 'gradlew.bat clean test jacocoTestReport pitest' (o `.\run-tests.ps1`).
3. Inyectar mutación en validación de pago vs precio.
Resultado esperado: Mutante M1 KILLED; al menos un escenario de Cucumber falla al detectar la alteración condicional.
Prioridad: Alta (P1)

**TC-MUT-003 — Eliminación de Mutante M2 — Operadores Matemáticos de Inventario**
Pasos:
1. Configurar PITest Math Mutator en Inventory.java.
2. Inyectar mutación cambiando resta por suma en deducción de stock.
3. Ejecutar PITest.
Resultado esperado: Mutante M2 KILLED; los steps de verificación de stock detectan la discrepancia numérica.
Prioridad: Alta (P1)

**TC-MUT-004 — Eliminación de Mutante M4 — Retorno Forzado de Valores (Void / Primitivos)**
Pasos:
1. Configurar PITest Boolean False Return en RecipeBook.addRecipe().
2. Forzar retorno false estático.
3. Ejecutar análisis.
Resultado esperado: Mutante M4 KILLED; los escenarios de catálogo de recetas detectan el retorno anómalo.
Prioridad: Media (P2)

**TC-MUT-005 — Eliminación de Mutantes M5 y M6 — Mutaciones de Límite y Colecciones**
Pasos:
1. Aplicar mutadores de límites e incrementos sobre arreglos en RecipeBook.java.
2. Ejecutar PITest y abrir reporte HTML.
Resultado esperado: Mutantes M5 y M6 KILLED; Mutation Score total >= 80% sin mutantes sobrevivientes en transacciones críticas.
Prioridad: Alta (P1)
