/*
 * Copyright (c) 2009,  Sarah Heckman, Laurie Williams, Dright Ho
 * All Rights Reserved.
 * 
 * Permission has been explicitly granted to the University of Minnesota 
 * Software Engineering Center to use and distribute this source for 
 * educational purposes, including delivering online education through
 * Coursera or other entities.  
 * 
 * No warranty is given regarding this software, including warranties as
 * to the correctness or completeness of this software, including 
 * fitness for purpose.
 * 
 * 
 * Modified 20171114 by Ian De Silva -- Updated to adhere to coding standards.
 * 
 */
package edu.ncsu.csc326.coffeemaker;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import static org.junit.Assert.assertNull;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.Then;
import cucumber.api.java.en.When;
import edu.ncsu.csc326.coffeemaker.CoffeeMakerUI.Mode;
import edu.ncsu.csc326.coffeemaker.CoffeeMakerUI.Status;
import edu.ncsu.csc326.coffeemaker.UICmd.AddInventory;
import edu.ncsu.csc326.coffeemaker.UICmd.CheckInventory;
import edu.ncsu.csc326.coffeemaker.UICmd.ChooseRecipe;
import edu.ncsu.csc326.coffeemaker.UICmd.ChooseService;
import edu.ncsu.csc326.coffeemaker.UICmd.DescribeRecipe;
import edu.ncsu.csc326.coffeemaker.UICmd.InsertMoney;
import edu.ncsu.csc326.coffeemaker.exceptions.InventoryException;
import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;
import edu.ncsu.csc326.coffeemaker.CoffeeMaker;

/**
 * Contains the step definitions for the cucumber tests.  This parses the 
 * Gherkin steps and translates them into meaningful test steps.
 */
public class TestSteps {
	
	private Recipe recipe1;
	private Recipe recipe2;
	private Recipe recipe3;
	private Recipe recipe4;
	private Recipe recipe5;
	private CoffeeMakerUI coffeeMakerMain; 
	private CoffeeMaker coffeeMaker;
	private RecipeBook recipeBook;
	private String inventoryReport;
	private int change;
	private int returnedMoney;

	private Recipe recipe(String name, String price, String coffee, String milk, String sugar, String chocolate) throws RecipeException {
		Recipe recipe = new Recipe();
		recipe.setName(name);
		recipe.setPrice(price);
		recipe.setAmtCoffee(coffee);
		recipe.setAmtMilk(milk);
		recipe.setAmtSugar(sugar);
		recipe.setAmtChocolate(chocolate);
		return recipe;
	}

	
	private void initialize() {
		recipeBook = new RecipeBook();
		coffeeMaker = new CoffeeMaker(recipeBook, new Inventory());
		coffeeMakerMain = new CoffeeMakerUI(coffeeMaker);
	}
	
    @Given("^an empty recipe book$")
    public void an_empty_recipe_book() throws Throwable {
        initialize();
    }


    @Given("a default recipe book")
    public void a_default_recipe_book() throws Throwable {
    	initialize();
    	
		//Set up for r1
		recipe1 = new Recipe();
		recipe1.setName("Coffee");
		recipe1.setAmtChocolate("0");
		recipe1.setAmtCoffee("3");
		recipe1.setAmtMilk("1");
		recipe1.setAmtSugar("1");
		recipe1.setPrice("50");
		
		//Set up for r2
		recipe2 = new Recipe();
		recipe2.setName("Mocha");
		recipe2.setAmtChocolate("20");
		recipe2.setAmtCoffee("3");
		recipe2.setAmtMilk("1");
		recipe2.setAmtSugar("1");
		recipe2.setPrice("75");
		
		//Set up for r3
		recipe3 = new Recipe();
		recipe3.setName("Latte");
		recipe3.setAmtChocolate("0");
		recipe3.setAmtCoffee("3");
		recipe3.setAmtMilk("3");
		recipe3.setAmtSugar("1");
		recipe3.setPrice("100");
		
		//Set up for r4
		recipe4 = new Recipe();
		recipe4.setName("Hot Chocolate");
		recipe4.setAmtChocolate("4");
		recipe4.setAmtCoffee("0");
		recipe4.setAmtMilk("1");
		recipe4.setAmtSugar("1");
		recipe4.setPrice("65");
		
		//Set up for r5 (added by MWW)
		recipe5 = new Recipe();
		recipe5.setName("Super Hot Chocolate");
		recipe5.setAmtChocolate("6");
		recipe5.setAmtCoffee("0");
		recipe5.setAmtMilk("1");
		recipe5.setAmtSugar("1");
		recipe5.setPrice("100");

		recipeBook.addRecipe(recipe1);
		recipeBook.addRecipe(recipe2);
		recipeBook.addRecipe(recipe3);
		recipeBook.addRecipe(recipe4);
		
	}

	@When("^I select every service from the waiting state$")
	public void selectEveryService() {
	    for (int button = 1; button <= 6; button++) {
	        initialize();
	        coffeeMakerMain.UI_Input(new ChooseService(button));
	        assertEquals(Mode.values()[button], coffeeMakerMain.getMode());
	    }
	    initialize();
	}

	@Then("^each service opens its expected mode$")
	public void servicesOpenExpectedModes() {
		assertEquals(Mode.WAITING, coffeeMakerMain.getMode());
	}

	@When("^I add a valid recipe through the interface$")
	public void addRecipeThroughUi() throws Throwable {
		coffeeMakerMain.UI_Input(new ChooseService(1));
		coffeeMakerMain.UI_Input(new DescribeRecipe(recipe("Espresso", "60", "3", "0", "1", "0")));
	}

	@Then("^the recipe is stored and the interface waits$")
	public void recipeIsStored() {
		assertEquals("Espresso", coffeeMakerMain.getRecipes()[0].getName());
		assertEquals(Status.OK, coffeeMakerMain.getStatus());
		assertEquals(Mode.WAITING, coffeeMakerMain.getMode());
	}

	@When("^I delete an existing recipe and try to delete an empty slot$")
	public void deleteExistingAndEmpty() throws Throwable {
		assertEquals("Coffee", coffeeMaker.deleteRecipe(0));
		assertEquals(null, coffeeMaker.deleteRecipe(0));
	}

	@Then("^deletion reports the correct outcomes$")
	public void deletionOutcomes() {
		assertEquals(null, coffeeMaker.getRecipes()[0]);
	}

	@When("^I edit an existing recipe and select an invalid recipe$")
	public void editAndInvalidSelect() throws Throwable {
		assertEquals("Coffee", coffeeMaker.editRecipe(0, recipe("Attempted new name", "40", "2", "2", "2", "2")));
		coffeeMakerMain.UI_Input(new ChooseService(3));
		coffeeMakerMain.UI_Input(new ChooseRecipe(4));
	}

	@Then("^editing preserves the recipe name and rejects the invalid selection$")
	public void editPreservesName() {
		assertEquals("Coffee", coffeeMaker.getRecipes()[0].getName());
		assertEquals(Status.OUT_OF_RANGE, coffeeMakerMain.getStatus());
		assertEquals(Mode.WAITING, coffeeMakerMain.getMode());
	}

	@When("^I add valid inventory and request the inventory report$")
	public void addAndCheckInventory() {
		coffeeMakerMain.UI_Input(new ChooseService(4));
		coffeeMakerMain.UI_Input(new AddInventory(2, 3, 4, 5));
		coffeeMakerMain.UI_Input(new ChooseService(5));
		CheckInventory command = new CheckInventory();
		coffeeMakerMain.UI_Input(command);
		inventoryReport = command.getInventory();
	}

	@When("^I request the inventory report$")
	public void requestInventoryReport() {
		coffeeMakerMain.UI_Input(new ChooseService(5));
		CheckInventory command = new CheckInventory();
		coffeeMakerMain.UI_Input(command);
		inventoryReport = command.getInventory();
	}

	@Then("^the inventory report contains the added amounts$")
	public void inventoryReportContainsAmounts() {
		assertTrue(inventoryReport.contains("Coffee:"));
		assertTrue(inventoryReport.contains("Milk:"));
		assertTrue(inventoryReport.contains("Sugar:"));
		assertTrue(inventoryReport.contains("Chocolate:"));
		assertEquals(Mode.WAITING, coffeeMakerMain.getMode());
	}

	@When("^I buy a recipe with enough money and then with insufficient money$")
	public void buyWithEnoughAndInsufficientMoney() throws Throwable {
		coffeeMakerMain.UI_Input(new ChooseService(6));
		coffeeMakerMain.UI_Input(new InsertMoney(75));
		coffeeMakerMain.UI_Input(new ChooseRecipe(0));
		change = coffeeMakerMain.getMoneyInTray();
		coffeeMakerMain.UI_Input(new ChooseService(6));
		coffeeMakerMain.UI_Input(new InsertMoney(10));
		coffeeMakerMain.UI_Input(new ChooseRecipe(0));
		returnedMoney = coffeeMakerMain.getMoneyInserted();
	}

	@Then("^the purchase returns change only for the successful purchase$")
	public void purchaseOutcomes() {
		assertEquals(25, change);
		assertEquals(10, returnedMoney);
		assertEquals(Status.INSUFFICIENT_FUNDS, coffeeMakerMain.getStatus());
	}

	@When("^I exercise recipe, inventory, and recipe book boundary cases$")
	public void exerciseDomainBoundaries() throws Throwable {
		Recipe valid = recipe("Valid", "10", "1", "2", "3", "4");
		assertEquals("Valid", valid.toString());
		assertTrue(valid.equals(recipe("Valid", "99", "0", "0", "0", "0")));
		assertFalse(valid.equals(recipe("Other", "10", "1", "2", "3", "4")));
		try { valid.setPrice("-1"); fail("Negative prices must be rejected"); } catch (RecipeException expected) { }
		try { valid.setAmtCoffee("abc"); fail("Non-numeric amounts must be rejected"); } catch (RecipeException expected) { }
		Inventory inventory = new Inventory();
		inventory.addCoffee("1"); inventory.addMilk("1"); inventory.addSugar("1"); inventory.addChocolate("1");
		assertEquals(16, inventory.getCoffee());
		assertEquals(16, inventory.getSugar());
		try { inventory.addChocolate("-1"); fail("Negative inventory must be rejected"); } catch (InventoryException expected) { }
		Recipe ingredients = recipe("Ingredients", "1", "2", "2", "2", "2");
		assertTrue(inventory.useIngredients(ingredients));
		assertEquals(14, inventory.getCoffee());
		inventory.setCoffee(0);
		assertFalse(inventory.useIngredients(ingredients));
		assertTrue(recipeBook.addRecipe(recipe("A", "1", "1", "1", "1", "1")));
		assertFalse(recipeBook.addRecipe(recipe("A", "2", "2", "2", "2", "2")));
		assertTrue(recipeBook.addRecipe(recipe("B", "1", "1", "1", "1", "1")));
		assertTrue(recipeBook.addRecipe(recipe("C", "1", "1", "1", "1", "1")));
		assertTrue(recipeBook.addRecipe(recipe("D", "1", "1", "1", "1", "1")));
		assertFalse(recipeBook.addRecipe(recipe("E", "1", "1", "1", "1", "1")));
	}

	@Then("^valid domain state is retained and invalid values are rejected$")
	public void domainStateIsRetained() {
		assertEquals(4, recipeBook.getRecipes().length);
	}
	
	@When("^I exercise the remaining interface and validation branches$")
	public void exerciseRemainingInterfaceAndValidationBranches() throws Throwable {
	    // Errores de conversión de cada atributo de Recipe
	    Recipe invalidRecipe = new Recipe();
	    try { invalidRecipe.setAmtChocolate("x"); fail("Expected RecipeException"); }
	    catch (RecipeException expected) { }
	    try { invalidRecipe.setAmtCoffee("x"); fail("Expected RecipeException"); }
	    catch (RecipeException expected) { }
	    try { invalidRecipe.setAmtMilk("x"); fail("Expected RecipeException"); }
	    catch (RecipeException expected) { }
	    try { invalidRecipe.setAmtSugar("x"); fail("Expected RecipeException"); }
	    catch (RecipeException expected) { }
	    try { invalidRecipe.setPrice("-1"); fail("Expected RecipeException"); }
	    catch (RecipeException expected) { }

	    Recipe sameOne = recipe("Same", "10", "1", "1", "1", "1");
	    Recipe sameTwo = recipe("Same", "20", "2", "2", "2", "2");
	    assertTrue(sameOne.equals(sameOne));
	    assertTrue(sameOne.equals(sameTwo));
	    assertFalse(sameOne.equals(null));
	    assertFalse(sameOne.equals("Same"));
	    assertTrue(sameOne.hashCode() != 0);

	    // Inventario: valores cero, positivos y no numéricos
	    Inventory inventory = new Inventory();
	    inventory.addCoffee("0");
	    inventory.addMilk("0");
	    inventory.addSugar("0");
	    inventory.addChocolate("0");
	    try { inventory.addChocolate("-1"); fail("Expected InventoryException"); }
	    catch (InventoryException expected) { }
	    try { inventory.addCoffee("bad"); fail("Expected InventoryException"); }
	    catch (InventoryException expected) { }
	    try { inventory.addMilk("bad"); fail("Expected InventoryException"); }
	    catch (InventoryException expected) { }
	    try { inventory.addSugar("bad"); fail("Expected InventoryException"); }
	    catch (InventoryException expected) { }
	    assertTrue(inventory.toString().contains("Coffee: 15"));

	    // UI: comando incorrecto al agregar receta y reinicio
	    initialize();
	    coffeeMakerMain.UI_Input(new ChooseService(1));
	    coffeeMakerMain.UI_Input(new InsertMoney(5));
	    assertEquals(Mode.ADD_RECIPE, coffeeMakerMain.getMode());
	    assertEquals(Status.OK, coffeeMakerMain.getStatus());
	    coffeeMakerMain.UI_Input(new edu.ncsu.csc326.coffeemaker.UICmd.Reset());
	    assertEquals(Mode.WAITING, coffeeMakerMain.getMode());

	    // UI: eliminar receta existente y receta inexistente
	    initialize();
	    coffeeMaker.addRecipe(recipe("Delete", "10", "1", "1", "1", "1"));
	    coffeeMakerMain.UI_Input(new ChooseService(2));
	    coffeeMakerMain.UI_Input(new ChooseRecipe(0));
	    assertEquals(Status.OK, coffeeMakerMain.getStatus());
	    assertEquals(Mode.WAITING, coffeeMakerMain.getMode());

	    coffeeMakerMain.UI_Input(new ChooseService(2));
	    coffeeMakerMain.UI_Input(new ChooseRecipe(0));
	    assertEquals(Status.OUT_OF_RANGE, coffeeMakerMain.getStatus());

	    // UI: consultar inventario y comando alternativo en ese modo
	    initialize();
	    coffeeMakerMain.displayRecipes();
	    coffeeMakerMain.UI_Input(new ChooseService(5));
	    coffeeMakerMain.UI_Input(new InsertMoney(3));
	    assertEquals(Mode.CHECK_INVENTORY, coffeeMakerMain.getMode());
	    assertEquals(3, coffeeMakerMain.getMoneyInserted());
	    coffeeMakerMain.UI_Input(new edu.ncsu.csc326.coffeemaker.UICmd.Reset());
	    assertEquals(Mode.WAITING, coffeeMakerMain.getMode());

	    // RecipeBook: edición válida y eliminación de posición vacía
	    RecipeBook book = new RecipeBook();
	    assertNull(book.deleteRecipe(0));
	    assertNull(book.editRecipe(0, recipe("Unused", "1", "1", "1", "1", "1")));
	    assertTrue(book.addRecipe(recipe("First", "10", "1", "1", "1", "1")));
	    assertEquals("First",
	        book.editRecipe(0, recipe("Changed", "20", "2", "2", "2", "2")));
	    assertEquals("First", book.getRecipes()[0].getName());
		// Recipe: ramas de valores negativos y precio no numérico
try { invalidRecipe.setAmtChocolate("-1"); fail("Expected RecipeException"); }
catch (RecipeException expected) { }
try { invalidRecipe.setAmtCoffee("-1"); fail("Expected RecipeException"); }
catch (RecipeException expected) { }
try { invalidRecipe.setAmtMilk("-1"); fail("Expected RecipeException"); }
catch (RecipeException expected) { }
try { invalidRecipe.setAmtSugar("-1"); fail("Expected RecipeException"); }
catch (RecipeException expected) { }
try { invalidRecipe.setPrice("bad"); fail("Expected RecipeException"); }
catch (RecipeException expected) { }

// Inventory: ramas negativas, texto inválido y faltantes de cada ingrediente
Inventory edgeInventory = new Inventory();
try { edgeInventory.addCoffee("-1"); fail("Expected InventoryException"); }
catch (InventoryException expected) { }
try { edgeInventory.addMilk("-1"); fail("Expected InventoryException"); }
catch (InventoryException expected) { }
try { edgeInventory.addSugar("-1"); fail("Expected InventoryException"); }
catch (InventoryException expected) { }
try { edgeInventory.addChocolate("bad"); fail("Expected InventoryException"); }
catch (InventoryException expected) { }

edgeInventory.setCoffee(20);
assertFalse(edgeInventory.enoughIngredients(
    recipe("NeedMilk", "1", "1", "16", "1", "1")));

edgeInventory.setMilk(20);
assertFalse(edgeInventory.enoughIngredients(
    recipe("NeedSugar", "1", "1", "1", "16", "1")));

edgeInventory.setSugar(20);
assertFalse(edgeInventory.enoughIngredients(
    recipe("NeedChocolate", "1", "1", "1", "1", "16")));

// CoffeeMaker: pago suficiente, pero inventario insuficiente
initialize();
coffeeMaker.addRecipe(recipe("NoStock", "10", "16", "1", "1", "1"));
assertEquals(10, coffeeMaker.makeCoffee(0, 10));
	}

	@Then("^all alternate flows preserve a valid state$")
	public void allAlternateFlowsPreserveAValidState() {
	    assertEquals(Mode.WAITING, coffeeMakerMain.getMode());
	}

	@When("^I exercise interface error handling and alternate purchase flows$")
public void exerciseInterfaceErrorHandlingAndAlternatePurchaseFlows() throws Throwable {
    exerciseRemainingInterfaceAndValidationBranches();
}

@Then("^the interface returns to a consistent waiting state$")
public void interfaceReturnsToAConsistentWaitingState() {
    assertEquals(Mode.WAITING, coffeeMakerMain.getMode());
}
    
}