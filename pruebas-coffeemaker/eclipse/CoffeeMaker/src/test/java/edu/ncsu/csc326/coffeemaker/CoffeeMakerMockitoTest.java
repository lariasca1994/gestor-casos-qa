package edu.ncsu.csc326.coffeemaker;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;
import org.junit.Before;
import org.junit.Test;

/**
 * Suite Mockito: CoffeeMaker recibe (RecipeBook, Inventory) por
 * constructor precisamente para poder inyectar aqui un RecipeBook
 * mockeado y probar CoffeeMaker sin depender de una implementacion real
 * del libro de recetas.
 */
public class CoffeeMakerMockitoTest {

    private RecipeBook recipeBookMock;
    private CoffeeMaker coffeeMaker;

    @Before
    public void setUp() {
        recipeBookMock = mock(RecipeBook.class);
        coffeeMaker = new CoffeeMaker(recipeBookMock, new Inventory());
    }

    @Test
    public void testGetRecipesDelegaEnRecipeBook() throws RecipeException {
        Recipe[] recetasEsperadas = { receta("Latte", "50", "3", "2", "1", "0") };
        when(recipeBookMock.getRecipes()).thenReturn(recetasEsperadas);

        Recipe[] recetas = coffeeMaker.getRecipes();

        assertEquals(recetasEsperadas, recetas);
        verify(recipeBookMock, times(1)).getRecipes();
    }

    @Test
    public void testAddRecipeDelegaEnRecipeBook() throws RecipeException {
        Recipe latte = receta("Latte", "50", "3", "2", "1", "0");
        when(recipeBookMock.addRecipe(latte)).thenReturn(true);

        boolean agregada = coffeeMaker.addRecipe(latte);

        assertEquals(true, agregada);
        verify(recipeBookMock).addRecipe(latte);
    }

    @Test
    public void testMakeCoffeeUsaLaRecetaQueDevuelveElMock() throws RecipeException {
        Recipe latte = receta("Latte", "50", "3", "2", "1", "0");
        when(recipeBookMock.getRecipes()).thenReturn(new Recipe[] { latte });

        int vuelto = coffeeMaker.makeCoffee(0, 100);

        assertEquals(50, vuelto);
        verify(recipeBookMock, times(1)).getRecipes();
    }

    @Test
    public void testMakeCoffeeConRecipeBookVacioNoDaVuelto() {
        when(recipeBookMock.getRecipes()).thenReturn(new Recipe[4]);

        int vuelto = coffeeMaker.makeCoffee(0, 100);

        assertEquals(100, vuelto);
    }

    @Test
    public void testMakeCoffeeDelegaConsumoEnInventoryMockeadoSiPagoAlcanza() throws RecipeException {
        // TC-MCK-002: se mockea Inventory (no solo RecipeBook) para
        // aislar CoffeeMaker.makeCoffee de la logica real de consumo.
        Inventory inventoryMock = mock(Inventory.class);
        CoffeeMaker cm = new CoffeeMaker(recipeBookMock, inventoryMock);
        Recipe latte = receta("Latte", "50", "3", "2", "1", "0");
        when(recipeBookMock.getRecipes()).thenReturn(new Recipe[] { latte });
        when(inventoryMock.useIngredients(any(Recipe.class))).thenReturn(true);

        int vuelto = cm.makeCoffee(0, 100);

        assertEquals(50, vuelto);
        verify(inventoryMock, times(1)).useIngredients(latte);
    }

    @Test
    public void testMakeCoffeeNoConsumeInventoryMockeadoSiPagoInsuficiente() throws RecipeException {
        // Complemento de TC-MCK-002: si el pago no alcanza, useIngredients
        // del Inventory mockeado no debe invocarse en absoluto.
        Inventory inventoryMock = mock(Inventory.class);
        CoffeeMaker cm = new CoffeeMaker(recipeBookMock, inventoryMock);
        Recipe latte = receta("Latte", "50", "3", "2", "1", "0");
        when(recipeBookMock.getRecipes()).thenReturn(new Recipe[] { latte });

        int vuelto = cm.makeCoffee(0, 20);

        assertEquals(20, vuelto);
        verify(inventoryMock, never()).useIngredients(any(Recipe.class));
    }

    @Test
    public void testDeleteRecipeDelegaEnRecipeBook() {
        when(recipeBookMock.deleteRecipe(0)).thenReturn("Latte");

        String borrada = coffeeMaker.deleteRecipe(0);

        assertEquals("Latte", borrada);
        assertFalse(borrada.isEmpty());
        verify(recipeBookMock).deleteRecipe(0);
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
