package edu.ncsu.csc326.coffeemaker;

import static org.junit.Assert.assertEquals;

import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;
import org.junit.Before;
import org.junit.Test;

/** Suite TS_PURCHASE_FLOW: comprar una bebida con makeCoffee, en sus
 * distintos caminos (pago exacto, con vuelto, insuficiente, sin
 * ingredientes, receta invalida). */
public class CoffeeMakerPurchaseTest {

    private CoffeeMaker coffeeMaker;

    @Before
    public void setUp() throws RecipeException {
        coffeeMaker = new CoffeeMaker();
        Recipe latte = new Recipe();
        latte.setName("Latte");
        latte.setPrice("50");
        latte.setAmtCoffee("3");
        latte.setAmtMilk("2");
        latte.setAmtSugar("1");
        latte.setAmtChocolate("0");
        coffeeMaker.addRecipe(latte);
    }

    @Test
    public void testPagoExacto() {
        int vuelto = coffeeMaker.makeCoffee(0, 50);
        assertEquals(0, vuelto);
    }

    @Test
    public void testPagoConVuelto() {
        int vuelto = coffeeMaker.makeCoffee(0, 100);
        assertEquals(50, vuelto);
    }

    @Test
    public void testPagoInsuficienteDevuelveTodoElDinero() {
        int vuelto = coffeeMaker.makeCoffee(0, 20);
        assertEquals(20, vuelto);
    }

    @Test
    public void testRecetaInexistenteDevuelveTodoElDinero() {
        int vuelto = coffeeMaker.makeCoffee(3, 50);
        assertEquals(50, vuelto);
    }

    @Test
    public void testIndiceFueraDeRangoDevuelveTodoElDinero() {
        int vuelto = coffeeMaker.makeCoffee(-1, 50);
        assertEquals(50, vuelto);
    }

    @Test
    public void testSinIngredientesSuficientesNoDescuentaElDinero() throws RecipeException {
        Recipe extraFuerte = new Recipe();
        extraFuerte.setName("Extra fuerte");
        extraFuerte.setPrice("60");
        extraFuerte.setAmtCoffee("100");
        extraFuerte.setAmtMilk("0");
        extraFuerte.setAmtSugar("0");
        extraFuerte.setAmtChocolate("0");
        coffeeMaker.addRecipe(extraFuerte);

        int vuelto = coffeeMaker.makeCoffee(1, 60);

        assertEquals(60, vuelto);
    }

    @Test
    public void testComprarDosVecesDescuentaInventarioAcumulado() {
        coffeeMaker.makeCoffee(0, 50);
        coffeeMaker.makeCoffee(0, 50);

        assertEquals(15 - 3 - 3, coffeeMaker.getInventory().getCoffee());
    }
}
