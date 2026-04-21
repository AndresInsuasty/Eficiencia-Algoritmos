from typing import List


def contar_inversiones(arr: List[int]) -> int:
    """
    Cuenta el número de inversiones en un arreglo.

    Una inversión es un par de índices (i, j) donde i < j pero arr[i] > arr[j].
    Esto es conceptualmente útil para medir cuán "desordenado" está un arreglo.

    Args:
        arr: Lista de números enteros

    Returns:
        Cantidad de inversiones encontradas

    Complexity:
        Time: O(n²) - Itera sobre todos los pares del arreglo
        Space: O(1) - Solo usa variables de conteo
    """
    contador = 0
    n = len(arr)

    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                contador += 1

    return contador


def encontrar_pares_suma(arr: List[int], objetivo: int) -> List[tuple[int, int]]:
    """
    Encuentra todos los pares (i, j) donde i < j y arr[i] + arr[j] == objetivo.

    Útil para entender problemas de búsqueda en O(n²).

    Args:
        arr: Lista de números enteros
        objetivo: Suma objetivo

    Returns:
        Lista de tuplas (índice_i, índice_j) que cumplen la condición

    Complexity:
        Time: O(n²) - Compara cada elemento con todos los demás
        Space: O(k) - k es la cantidad de pares encontrados
    """
    pares = []

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == objetivo:
                pares.append((i, j))

    return pares


def contar_comparaciones(arr: List[int], objetivo: int) -> tuple[int, int]:
    """
    Cuenta pares donde arr[i] > objetivo (comparación O(n²)).

    Retorna el conteo total y el número de comparaciones realizadas.

    Args:
        arr: Lista de números enteros
        objetivo: Valor a comparar

    Returns:
        Tupla (cantidad_de_pares, total_de_comparaciones)

    Complexity:
        Time: O(n²) - Compara cada elemento con todos los demás
        Space: O(1)
    """
    contador_pares = 0
    total_comparaciones = 0

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            total_comparaciones += 1
            if arr[i] > objetivo and arr[j] > objetivo:
                contador_pares += 1

    return contador_pares, total_comparaciones
