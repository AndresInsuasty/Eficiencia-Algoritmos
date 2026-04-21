from typing import List
from dataclasses import dataclass
import math


@dataclass
class Punto:
    """Representa un punto en el plano 2D."""
    x: float
    y: float


@dataclass
class Circulo:
    """Representa un círculo con centro y radio."""
    centro: Punto
    radio: float


def distancia_entre_puntos(p1: Punto, p2: Punto) -> float:
    """Calcula la distancia euclidiana entre dos puntos."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def circulos_colisionan(c1: Circulo, c2: Circulo) -> bool:
    """
    Determina si dos círculos colisionan.

    Dos círculos colisionan si la distancia entre sus centros es menor
    o igual a la suma de sus radios.

    Args:
        c1: Primer círculo
        c2: Segundo círculo

    Returns:
        True si los círculos colisionan, False si no
    """
    distancia = distancia_entre_puntos(c1.centro, c2.centro)
    return distancia <= (c1.radio + c2.radio)


def contar_colisiones(circulos: List[Circulo]) -> int:
    """
    Cuenta el número total de colisiones entre N círculos.

    Verifica cada círculo contra todos los demás para detectar colisiones.

    Args:
        circulos: Lista de círculos

    Returns:
        Cantidad de pares de círculos que colisionan

    Complexity:
        Time: O(n²) - Compara cada círculo con todos los otros círculos
        Space: O(1) - Solo usa variables de conteo
    """
    contador = 0
    n = len(circulos)

    for i in range(n):
        for j in range(i + 1, n):
            if circulos_colisionan(circulos[i], circulos[j]):
                contador += 1

    return contador


def obtener_pares_colisionados(circulos: List[Circulo]) -> List[tuple[int, int]]:
    """
    Obtiene todos los pares de índices que colisionan.

    Args:
        circulos: Lista de círculos

    Returns:
        Lista de tuplas (índice_i, índice_j) de círculos que colisionan

    Complexity:
        Time: O(n²) - Compara cada círculo con todos los otros
        Space: O(k) - k es la cantidad de colisiones encontradas
    """
    pares = []
    n = len(circulos)

    for i in range(n):
        for j in range(i + 1, n):
            if circulos_colisionan(circulos[i], circulos[j]):
                pares.append((i, j))

    return pares
