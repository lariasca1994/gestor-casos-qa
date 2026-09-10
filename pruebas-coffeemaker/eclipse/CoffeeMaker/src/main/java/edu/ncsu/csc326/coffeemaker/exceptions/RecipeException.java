package edu.ncsu.csc326.coffeemaker.exceptions;

/**
 * Se lanza cuando los datos de una Recipe no son validos (precio o
 * cantidad de un ingrediente negativos, o que no son un numero entero).
 */
public class RecipeException extends Exception {

    private static final long serialVersionUID = 1L;

    public RecipeException(String mensaje) {
        super(mensaje);
    }
}
