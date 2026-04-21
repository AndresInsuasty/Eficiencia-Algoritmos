from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Bubble Sort.

    Compara elementos adyacentes y los intercambia si están en orden incorrecto.
    El proceso se repite hasta que el arreglo está completamente ordenado.

    Args:
        arr: Lista de números enteros a ordenar

    Returns:
        Lista ordenada

    Complexity:
        Time: O(n²) - En el peor caso, realiza n-1 pasadas sobre el arreglo
        Space: O(1) - Ordena in-place
    """
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def merge_sort(arr: List[int]) -> List[int]:
    """
    Ordena un arreglo usando el algoritmo Merge Sort (divide y conquista).

    Divide el arreglo en mitades recursivamente y luego las fusiona ordenadamente.

    Args:
        arr: Lista de números enteros a ordenar

    Returns:
        Lista ordenada

    Complexity:
        Time: O(n log n) - Divide (log n) y luego fusiona (n) en cada nivel
        Space: O(n) - Requiere espacio adicional para la fusión
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    izq = merge_sort(arr[:mid])
    der = merge_sort(arr[mid:])

    return _merge(izq, der)


def _merge(izq: List[int], der: List[int]) -> List[int]:
    """Función auxiliar para fusionar dos arreglos ordenados."""
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado
