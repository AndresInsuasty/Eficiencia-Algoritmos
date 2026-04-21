def es_par_impar(numero: int=10) -> str:
    """
    Determina si un número es par o impar.

    Args:
        numero: Número entero a verificar

    Returns:
        String indicando si el número es "par" o "impar"

    Complexity:
        Time: O(1)
        Space: O(1)
    """
    return "par" if numero % 2 == 0 else "impar"
