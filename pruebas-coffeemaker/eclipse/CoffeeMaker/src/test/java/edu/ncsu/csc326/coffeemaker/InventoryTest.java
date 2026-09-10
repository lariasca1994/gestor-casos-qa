package edu.ncsu.csc326.coffeemaker;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import edu.ncsu.csc326.coffeemaker.exceptions.InventoryException;
import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;
import org.junit.Before;
import org.junit.Test;

/** Suite TS_INVENTORY_MGMT: agregar ingredientes y descontar el
 * inventario al preparar una receta. */
public class InventoryTest {

    private Inventory inventory;

    @Before
    public void setUp() {
        inventory = new Inventory();
    }

    @Test
    public void testInventarioInicial() {
        assertEquals(15, inventory.getCoffee());
        assertEquals(15, inventory.getMilk());
        assertEquals(15, inventory.getSugar());
        assertEquals(15, inventory.getChocolate());
    }

    @Test
    public void testAddCoffeeValido() throws InventoryException {
        inventory.addCoffee("10");
        assertEquals(25, inventory.getCoffee());
    }

    @Test(expected = InventoryException.class)
    public void testAddCoffeeNegativo() throws InventoryException {
        inventory.addCoffee("-10");
    }

    @Test(expected = InventoryException.class)
    public void testAddSugarNoNumerico() throws InventoryException {
        inventory.addSugar("mucho");
    }

    @Test
    public void testEnoughIngredientsConSuficiente() throws RecipeException {
        Recipe receta = recetaValida();
        assertTrue(inventory.enoughIngredients(receta));
    }

    @Test
    public void testEnoughIngredientsInsuficiente() throws RecipeException {
        Recipe receta = new Recipe();
        receta.setName("Extra fuerte");
        receta.setPrice("60");
        receta.setAmtCoffee("100");
        receta.setAmtMilk("0");
        receta.setAmtSugar("0");
        receta.setAmtChocolate("0");
        assertFalse(inventory.enoughIngredients(receta));
    }

    @Test
    public void testUseIngredientsDescuentaCorrectamente() throws RecipeException {
        Recipe receta = recetaValida();
        boolean usado = inventory.useIngredients(receta);
        assertTrue(usado);
        assertEquals(15 - receta.getAmtCoffee(), inventory.getCoffee());
        assertEquals(15 - receta.getAmtMilk(), inventory.getMilk());
        assertEquals(15 - receta.getAmtSugar(), inventory.getSugar());
        assertEquals(15 - receta.getAmtChocolate(), inventory.getChocolate());
    }

    @Test
    public void testUseIngredientsNoDescuentaSiNoAlcanza() throws RecipeException {
        Recipe receta = new Recipe();
        receta.setName("Extra fuerte");
        receta.setPrice("60");
        receta.setAmtCoffee("100");
        receta.setAmtMilk("0");
        receta.setAmtSugar("0");
        receta.setAmtChocolate("0");

        boolean usado = inventory.useIngredients(receta);

        assertFalse(usado);
        // el inventario no debe quedar tocado
        assertEquals(15, inventory.getCoffee());
    }

    private Recipe recetaValida() throws RecipeException {
        Recipe receta = new Recipe();
        receta.setName("Latte");
        receta.setPrice("50");
        receta.setAmtCoffee("3");
        receta.setAmtMilk("2");
        receta.setAmtSugar("1");
        receta.setAmtChocolate("0");
        return receta;
    }
}
