package edu.ncsu.csc326.coffeemaker;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;
import org.junit.Before;
import org.junit.Test;

/** Pruebas de validacion de Recipe: cada setter debe rechazar valores
 * negativos o que no sean un numero entero. */
public class RecipeTest {

    private Recipe recipe;

    @Before
    public void setUp() {
        recipe = new Recipe();
    }

    @Test
    public void testSetPrecioValido() throws RecipeException {
        recipe.setPrice("50");
        assertEquals(50, recipe.getPrice());
    }

    @Test
    public void testSetPrecioNegativo() {
        try {
            recipe.setPrice("-1");
            fail("Debia lanzar RecipeException con precio negativo");
        } catch (RecipeException e) {
            assertTrue(e.getMessage().contains("negativa"));
        }
    }

    @Test
    public void testSetPrecioNoNumerico() {
        try {
            recipe.setPrice("gratis");
            fail("Debia lanzar RecipeException con precio no numerico");
        } catch (RecipeException e) {
            assertTrue(e.getMessage().contains("numero entero"));
        }
    }

    @Test
    public void testSetCantidadesValidas() throws RecipeException {
        recipe.setAmtCoffee("3");
        recipe.setAmtMilk("1");
        recipe.setAmtSugar("2");
        recipe.setAmtChocolate("0");
        assertEquals(3, recipe.getAmtCoffee());
        assertEquals(1, recipe.getAmtMilk());
        assertEquals(2, recipe.getAmtSugar());
        assertEquals(0, recipe.getAmtChocolate());
    }

    @Test(expected = RecipeException.class)
    public void testSetCantidadCafeNegativa() throws RecipeException {
        recipe.setAmtCoffee("-3");
    }

    @Test(expected = RecipeException.class)
    public void testSetCantidadLecheNoNumerica() throws RecipeException {
        recipe.setAmtMilk("mucha");
    }

    @Test
    public void testEqualsPorNombre() {
        recipe.setName("Latte");
        Recipe otra = new Recipe();
        otra.setName("Latte");
        assertTrue(recipe.equals(otra));
        assertEquals(recipe.hashCode(), otra.hashCode());
    }

    @Test
    public void testNoEqualsConNombreDistinto() {
        recipe.setName("Latte");
        Recipe otra = new Recipe();
        otra.setName("Mocha");
        assertFalse(recipe.equals(otra));
    }
}
