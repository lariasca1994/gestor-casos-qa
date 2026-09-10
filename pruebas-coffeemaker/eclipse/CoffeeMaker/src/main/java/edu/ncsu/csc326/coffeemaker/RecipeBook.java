package edu.ncsu.csc326.coffeemaker;

/**
 * Contrato del libro de recetas. Se dejo como interfaz (en vez de una
 * clase concreta) para poder mockearla con Mockito en las pruebas de
 * CoffeeMaker sin depender de una implementacion real.
 */
public interface RecipeBook {

    Recipe[] getRecipes();

    boolean addRecipe(Recipe recipe);

    String deleteRecipe(int recipeToDelete);

    String editRecipe(int recipeToEdit, Recipe newRecipe);
}
