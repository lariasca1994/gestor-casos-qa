package edu.ncsu.csc326.coffeemaker;

/**
 * Orquesta el libro de recetas y el inventario. El constructor con
 * (RecipeBook, Inventory) permite inyectar dobles de prueba -- es el
 * que se usa en las pruebas con Mockito.
 */
public class CoffeeMaker {

    private final RecipeBook recipeBook;
    private final Inventory inventory;

    public CoffeeMaker() {
        this(new RecipeBookImpl(), new Inventory());
    }

    public CoffeeMaker(RecipeBook recipeBook, Inventory inventory) {
        this.recipeBook = recipeBook;
        this.inventory = inventory;
    }

    public boolean addRecipe(Recipe recipe) {
        return recipeBook.addRecipe(recipe);
    }

    public String deleteRecipe(int recipeToDelete) {
        return recipeBook.deleteRecipe(recipeToDelete);
    }

    public String editRecipe(int recipeToEdit, Recipe newRecipe) {
        return recipeBook.editRecipe(recipeToEdit, newRecipe);
    }

    public Recipe[] getRecipes() {
        return recipeBook.getRecipes();
    }

    public Inventory getInventory() {
        return inventory;
    }

    /**
     * Intenta preparar la receta en la posicion recipeToPurchase.
     * Devuelve el vuelto si alcanzo el pago y habia ingredientes; si no,
     * devuelve el pago completo sin cobrar nada (no se descuenta
     * inventario ni se hace la bebida).
     */
    public int makeCoffee(int recipeToPurchase, int amtPaid) {
        Recipe[] recipes = recipeBook.getRecipes();
        if (recipeToPurchase < 0 || recipeToPurchase >= recipes.length) {
            return amtPaid;
        }
        Recipe recipe = recipes[recipeToPurchase];
        if (recipe == null) {
            return amtPaid;
        }
        if (amtPaid < recipe.getPrice()) {
            return amtPaid;
        }
        if (!inventory.useIngredients(recipe)) {
            return amtPaid;
        }
        return amtPaid - recipe.getPrice();
    }
}
