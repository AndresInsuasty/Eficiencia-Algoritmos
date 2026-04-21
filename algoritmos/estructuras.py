from collections import deque
from typing import List


def llenar_pila(n: int) -> List[int]:
    """
    Llena una pila (stack) con n elementos.

    Args:
        n: Cantidad de elementos a agregar

    Returns:
        Lista que actúa como pila con n elementos

    Complexity:
        Time: O(n)
        Space: O(n)
    """
    pila = []
    for i in range(n):
        pila.append(i)
    return pila


def llenar_cola(n: int) -> deque:
    """
    Llena una cola (queue) con n elementos.

    Args:
        n: Cantidad de elementos a agregar

    Returns:
        Deque que actúa como cola con n elementos

    Complexity:
        Time: O(n)
        Space: O(n)
    """
    cola = deque()
    for i in range(n):
        cola.append(i)
    return cola


def vaciar_pila(pila: List[int]) -> List[int]:
    """
    Vacía una pila extrayendo todos los elementos (LIFO).

    Args:
        pila: Pila a vaciar

    Returns:
        Lista con los elementos extraídos

    Complexity:
        Time: O(n)
        Space: O(n)
    """
    resultado = []
    while pila:
        resultado.append(pila.pop())
    return resultado


def vaciar_cola(cola: deque) -> List[int]:
    """
    Vacía una cola extrayendo todos los elementos (FIFO).

    Args:
        cola: Cola a vaciar

    Returns:
        Lista con los elementos extraídos

    Complexity:
        Time: O(n)
        Space: O(n)
    """
    resultado = []
    while cola:
        resultado.append(cola.popleft())
    return resultado
