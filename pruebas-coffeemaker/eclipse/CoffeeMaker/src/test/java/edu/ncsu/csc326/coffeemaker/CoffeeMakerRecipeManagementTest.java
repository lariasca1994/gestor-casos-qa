package edu.ncsu.csc326.coffeemaker;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;
import org.junit.Before;
import org.junit.Test;

/** Suite TS_RECIPE_MGMT: agregar, editar y borrar recetas del libro. */
public class CoffeeMakerRecipeManagementTest {

    private CoffeeMaker coffeeMaker;

    @Before
    public void setUp() {
        coffeeMaker = new CoffeeMaker();
    }

    @Test
    public void testAgregarRecetaValida() throws RecipeException {
        assertTrue(coffeeMaker.addRecipe(receta("Coffee", "50", "3", "1", "1", "0")));
        assertEquals("Coffee", coffeeMaker.getRecipes()[0].getName());
    }

    @Test
    public void testNoAgregarRecetaDuplicada() throws RecipeException {
        coffeeMaker.addRecipe(receta("Coffee", "50", "3", "1", "1", "0"));
        boolean segundaVez = coffeeMaker.addRecipe(receta("Coffee", "60", "2", "1", "1", "0"));
        assertFalse(segundaVez);
    }

    @Test
    public void testNoAgregarRecetaSiLibroLleno() throws RecipeException {
        coffeeMaker.addRecipe(receta("Coffee", "50", "3", "1", "1", "0"));
        coffeeMaker.addRecipe(receta("Mocha", "70", "3", "1", "1", "2"));
        coffeeMaker.addRecipe(receta("Latte", "60", "3", "2", "1", "0"));
        coffeeMaker.addRecipe(receta("Hot Chocolate", "50", "0", "1", "1", "3"));

        boolean quinta = coffeeMaker.addRecipe(receta("Espresso", "40", "4", "0", "0", "0"));

        assertFalse(quinta);
    }

    @Test
    public void testEditarRecetaExistente() throws RecipeException {
        coffeeMaker.addRecipe(receta("Coffee", "50", "3", "1", "1", "0"));
        String nombreAnterior = coffeeMaker.editRecipe(0, receta("Coffee Fuerte", "55", "4", "1", "1", "0"));
        assertEquals("Coffee", nombreAnterior);
        assertEquals("Coffee Fuerte", coffeeMaker.getRecipes()[0].getName());
    }

    @Test
    public void testEditarPosicionVaciaDevuelveNull() throws RecipeException {
        String resultado = coffeeMaker.editRecipe(2, receta("Latte", "60", "3", "2", "1", "0"));
        assertNull(resultado);
    }

    @Test
    public void testBorrarRecetaExistente() throws RecipeException {
        coffeeMaker.addRecipe(receta("Coffee", "50", "3", "1", "1", "0"));
        String borrada = coffeeMaker.deleteRecipe(0);
        assertEquals("Coffee", borrada);
        assertNull(coffeeMaker.getRecipes()[0]);
    }

    @Test
    public void testBorrarPosicionVaciaDevuelveNull() {
        assertNull(coffeeMaker.deleteRecipe(1));
    }

    private Recipe receta(String nombre, String precio, String cafe, String leche, String azucar, String chocolate)
            throws RecipeException {
        Recipe r = new Recipe();
        r.setName(nombre);
        r.setPrice(precio);
        r.setAmtCoffee(cafe);
        r.setAmtMilk(leche);
        r.setAmtSugar(azucar);
        r.setAmtChocolate(chocolate);
        return r;
    }
}
