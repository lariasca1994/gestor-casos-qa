# CoffeeMaker — JUnit + Mockito + JaCoCo

Proyecto Java (Maven) sobre el clasico ejercicio **CoffeeMaker** de la
especializacion de Coursera "Introducción a las pruebas de software"
(Universidad de Minnesota). Reconstruido como un solo proyecto consolidado
para el portafolio, con tres tecnicas de prueba trabajando sobre el mismo
codigo:

- **JUnit** — pruebas de comportamiento sobre `Recipe`, `Inventory` y
  `CoffeeMaker` (gestion de recetas, manejo de inventario, flujo de compra).
- **Mockito** — `CoffeeMaker` recibe `RecipeBook` (una interfaz) e
  `Inventory` por constructor, precisamente para poder inyectar un
  `RecipeBook` mockeado y probar `CoffeeMaker` de forma aislada.
- **JaCoCo** — mide la cobertura de ramas de las cuatro clases de dominio
  al correr la suite completa.

## Estructura

```
src/main/java/edu/ncsu/csc326/coffeemaker/
    Recipe.java            receta: nombre, precio, ingredientes
    RecipeBook.java         interfaz del libro de recetas (mockeable)
    RecipeBookImpl.java     implementacion real (arreglo de 4 recetas)
    Inventory.java          inventario de ingredientes
    CoffeeMaker.java        orquesta RecipeBook + Inventory
    exceptions/             RecipeException, InventoryException

src/test/java/edu/ncsu/csc326/coffeemaker/
    RecipeTest.java                     validaciones de Recipe
    InventoryTest.java                  suite TS_INVENTORY_MGMT
    CoffeeMakerRecipeManagementTest.java suite TS_RECIPE_MGMT
    CoffeeMakerPurchaseTest.java         suite TS_PURCHASE_FLOW
    CoffeeMakerMockitoTest.java          suite Mockito (mockea RecipeBook e Inventory)
```

**Verificado:** 37 tests, 0 fallos (7 Recipe... en realidad 7+7+7+8+8, ver
tabla abajo), reporte JaCoCo generado sin errores.

| Clase de test | Tests | Suite en la matriz |
|---|---|---|
| `RecipeTest` | 8 | validaciones de `Recipe` |
| `InventoryTest` | 8 | `TS_INVENTORY_MGMT` |
| `CoffeeMakerRecipeManagementTest` | 7 | `TS_RECIPE_MGMT` |
| `CoffeeMakerPurchaseTest` | 7 | `TS_PURCHASE_FLOW` |
| `CoffeeMakerMockitoTest` | 7 | `TS_MOCKITO_ISOLATION` (mockea `RecipeBook` y, en 2 tests, tambien `Inventory`) |

## Como correrlo

Requiere JDK 17+ y Maven (o Eclipse con m2e).

**Opcion A — desde PowerShell**, parado en esta carpeta:

```
.\run-tests.ps1
```

o directamente `mvn test`. (Si usas la terminal Git Bash integrada de
Eclipse y te da `mvn: command not found`, es porque esa terminal no tiene
Maven en su PATH — usa PowerShell, o la opcion B).

**Opcion B — desde Eclipse**: click derecho sobre el proyecto `coffeemaker`
en el Package Explorer > `Run As` > `Maven test`. Usa el Maven/JDK
embebido de Eclipse (m2e), sin depender del PATH de ninguna terminal.

Cualquiera de las dos compila, corre las 5 clases de test (37 tests en
total) y deja el reporte de JaCoCo listo, sin pasos adicionales, en:

```
target/site/jacoco/index.html          (cobertura)
target/surefire-reports/               (resultado por clase, uno por archivo .txt/.xml)
```

### Importar en Eclipse

`File > Import > Maven > Existing Maven Projects`, selecciona esta
carpeta. Eclipse (via m2e) descarga las dependencias y genera su propio
`.classpath`/`.project` — no hace falta traerlos del proyecto original.

## Sin datos sensibles

Este proyecto no se conecta a ninguna base de datos ni servicio externo:
es una libreria de dominio con sus pruebas. No requiere variables de
entorno ni credenciales.
