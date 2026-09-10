package edu.ncsu.csc326.coffeemaker;

import edu.ncsu.csc326.coffeemaker.exceptions.InventoryException;

/**
 * Inventario de ingredientes (cafe, leche, azucar, chocolate). Arranca
 * con 15 unidades de cada uno, como en la maquina real.
 */
public class Inventory {

    private int coffee;
    private int milk;
    private int sugar;
    private int chocolate;

    public Inventory() {
        coffee = 15;
        milk = 15;
        sugar = 15;
        chocolate = 15;
    }

    public void addCoffee(String amount) throws InventoryException {
        coffee += parsePositiveInt(amount, "cafe");
    }

    public void addMilk(String amount) throws InventoryException {
        milk += parsePositiveInt(amount, "leche");
    }

    public void addSugar(String amount) throws InventoryException {
        sugar += parsePositiveInt(amount, "azucar");
    }

    public void addChocolate(String amount) throws InventoryException {
        chocolate += parsePositiveInt(amount, "chocolate");
    }

    /** true si hay suficiente de cada ingrediente para preparar la receta. */
    public boolean enoughIngredients(Recipe recipe) {
        return coffee >= recipe.getAmtCoffee()
                && milk >= recipe.getAmtMilk()
                && sugar >= recipe.getAmtSugar()
                && chocolate >= recipe.getAmtChocolate();
    }

    /**
     * Descuenta del inventario lo que pide la receta, solo si alcanza.
     * Devuelve false (y no toca el inventario) si no hay suficiente.
     */
    public boolean useIngredients(Recipe recipe) {
        if (!enoughIngredients(recipe)) {
            return false;
        }
        coffee -= recipe.getAmtCoffee();
        milk -= recipe.getAmtMilk();
        sugar -= recipe.getAmtSugar();
        chocolate -= recipe.getAmtChocolate();
        return true;
    }

    public int getCoffee() {
        return coffee;
    }

    public int getMilk() {
        return milk;
    }

    public int getSugar() {
        return sugar;
    }

    public int getChocolate() {
        return chocolate;
    }

    private int parsePositiveInt(String valor, String etiqueta) throws InventoryException {
        int cantidad;
        try {
            cantidad = Integer.parseInt(valor);
        } catch (NumberFormatException | NullPointerException e) {
            throw new InventoryException("La cantidad de " + etiqueta + " debe ser un numero entero");
        }
        if (cantidad < 0) {
            throw new InventoryException("La cantidad de " + etiqueta + " no puede ser negativa");
        }
        return cantidad;
    }

    @Override
    public String toString() {
        return "Cafe: " + coffee
                + "\nLeche: " + milk
                + "\nAzucar: " + sugar
                + "\nChocolate: " + chocolate;
    }
}
