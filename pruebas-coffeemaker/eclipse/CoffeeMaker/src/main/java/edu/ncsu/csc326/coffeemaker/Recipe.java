package edu.ncsu.csc326.coffeemaker;

import edu.ncsu.csc326.coffeemaker.exceptions.RecipeException;

/**
 * Una receta de bebida: su nombre, precio, y la cantidad de cada
 * ingrediente que necesita. Todos los setters validan que el valor
 * recibido sea un numero entero no negativo.
 */
public class Recipe {

    private String name;
    private int price;
    private int amtCoffee;
    private int amtMilk;
    private int amtSugar;
    private int amtChocolate;

    public Recipe() {
        this.name = "";
        this.price = 0;
        this.amtCoffee = 0;
        this.amtMilk = 0;
        this.amtSugar = 0;
        this.amtChocolate = 0;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getPrice() {
        return price;
    }

    public void setPrice(String price) throws RecipeException {
        this.price = parsePositiveInt(price, "precio");
    }

    public int getAmtCoffee() {
        return amtCoffee;
    }

    public void setAmtCoffee(String amtCoffee) throws RecipeException {
        this.amtCoffee = parsePositiveInt(amtCoffee, "cantidad de cafe");
    }

    public int getAmtMilk() {
        return amtMilk;
    }

    public void setAmtMilk(String amtMilk) throws RecipeException {
        this.amtMilk = parsePositiveInt(amtMilk, "cantidad de leche");
    }

    public int getAmtSugar() {
        return amtSugar;
    }

    public void setAmtSugar(String amtSugar) throws RecipeException {
        this.amtSugar = parsePositiveInt(amtSugar, "cantidad de azucar");
    }

    public int getAmtChocolate() {
        return amtChocolate;
    }

    public void setAmtChocolate(String amtChocolate) throws RecipeException {
        this.amtChocolate = parsePositiveInt(amtChocolate, "cantidad de chocolate");
    }

    private int parsePositiveInt(String valor, String etiqueta) throws RecipeException {
        int cantidad;
        try {
            cantidad = Integer.parseInt(valor);
        } catch (NumberFormatException | NullPointerException e) {
            throw new RecipeException("La " + etiqueta + " debe ser un numero entero");
        }
        if (cantidad < 0) {
            throw new RecipeException("La " + etiqueta + " no puede ser negativa");
        }
        return cantidad;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (!(obj instanceof Recipe)) {
            return false;
        }
        Recipe otra = (Recipe) obj;
        return name != null && name.equals(otra.name);
    }

    @Override
    public int hashCode() {
        return name == null ? 0 : name.hashCode();
    }

    @Override
    public String toString() {
        return name;
    }
}
