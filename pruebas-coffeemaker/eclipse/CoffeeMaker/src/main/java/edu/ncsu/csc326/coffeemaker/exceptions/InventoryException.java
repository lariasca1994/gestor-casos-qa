package edu.ncsu.csc326.coffeemaker.exceptions;

/**
 * Se lanza cuando se intenta agregar al inventario una cantidad invalida
 * (negativa o que no es un numero entero).
 */
public class InventoryException extends Exception {

    private static final long serialVersionUID = 1L;

    public InventoryException(String mensaje) {
        super(mensaje);
    }
}
