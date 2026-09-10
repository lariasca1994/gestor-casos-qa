package edu.ncsu.csc326.coffeemaker;

/**
 * Implementacion real de RecipeBook: guarda hasta NUM_RECIPES recetas en
 * un arreglo de tamano fijo.
 */
public class RecipeBookImpl implements RecipeBook {

    public static final int NUM_RECIPES = 4;

    private final Recipe[] recipes;

    public RecipeBookImpl() {
        recipes = new Recipe[NUM_RECIPES];
    }

    @Override
    public Recipe[] getRecipes() {
        return recipes;
    }

    @Override
    public boolean addRecipe(Recipe recipe) {
        for (Recipe existente : recipes) {
            if (recipe.equals(existente)) {
                return false; // ya hay una receta con ese nombre
            }
        }
        for (int i = 0; i < recipes.length; i++) {
            if (recipes[i] == null) {
                recipes[i] = recipe;
                return true;
            }
        }
        return false; // libro lleno
    }

    @Override
    public String deleteRecipe(int recipeToDelete) {
        if (!indiceValido(recipeToDelete) || recipes[recipeToDelete] == null) {
            return null;
        }
        String nombreEliminado = recipes[recipeToDelete].getName();
        recipes[recipeToDelete] = null;
        return nombreEliminado;
    }

    @Override
    public String editRecipe(int recipeToEdit, Recipe newRecipe) {
        if (!indiceValido(recipeToEdit) || recipes[recipeToEdit] == null) {
            return null;
        }
        String nombreAnterior = recipes[recipeToEdit].getName();
        recipes[recipeToEdit] = newRecipe;
        return nombreAnterior;
    }

    private boolean indiceValido(int indice) {
        return indice >= 0 && indice < recipes.length;
    }
}
