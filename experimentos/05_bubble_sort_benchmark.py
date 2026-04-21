import time
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.ordenamiento import bubble_sort


def medir_tiempo_bubble_sort(tamaño: int, repeticiones: int = 5) -> float:
    """
    Mide el tiempo total para ejecutar bubble sort.

    Args:
        tamaño: Cantidad de números en el arreglo
        repeticiones: Veces a repetir la operación

    Returns:
        Tiempo total en microsegundos
    """
    arreglo = [random.randint(1, 10000) for _ in range(tamaño)]

    inicio = time.perf_counter()
    for _ in range(repeticiones):
        bubble_sort(arreglo)
    fin = time.perf_counter()

    tiempo_total = fin - inicio
    return tiempo_total * 1e6


def benchmark():
    """Ejecuta el benchmark midiendo tiempo vs tamaño del arreglo."""
    print("Iniciando benchmark de Bubble Sort...")
    print(f"Rango de tamaño: 50 a 1,000 elementos\n")

    # Generar tamaños de arreglos (espaciados logarítmicamente)
    tamaños = np.logspace(1.7, 3, 30, dtype=int)  # 50 a 1,000
    tamaños = sorted(list(set(tamaños)))

    tiempos = []

    print("Midiendo tiempos...")
    for i, tamaño in enumerate(tamaños):
        print(f"Progreso: {i+1}/{len(tamaños)} - Tamaño: {tamaño:,} elementos", end="\r")
        tiempo = medir_tiempo_bubble_sort(tamaño, repeticiones=3)
        tiempos.append(tiempo)

    print("\n\nGenerando gráfica...")

    # Crear scatter plot
    plt.figure(figsize=(12, 7))
    plt.scatter(tamaños, tiempos, alpha=0.7, s=50, color='#FF6B6B', edgecolors='darkred', linewidth=1)

    plt.xlabel('Tamaño del Arreglo (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Tiempo Total (microsegundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: Bubble Sort - Complejidad O(n²)', fontsize=14, fontweight='bold')

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'bubble_sort_benchmark.png')
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {img_path}")

    plt.show()

    # Mostrar estadísticas
    print("\n--- Estadísticas ---")
    print(f"Tiempo total mínimo: {min(tiempos):.2f} microsegundos")
    print(f"Tiempo total máximo: {max(tiempos):.2f} microsegundos")

    # Mostrar algunos puntos de datos
    print("\n--- Muestra de Datos ---")
    print("Tamaño (n) | Tiempo (µs)   | Tiempo/n² (µs)")
    print("-" * 50)
    for tamaño, tiempo in zip(tamaños[::max(1, len(tamaños)//8)], tiempos[::max(1, len(tamaños)//8)]):
        tiempo_por_n2 = tiempo / (tamaño ** 2)
        print(f"{tamaño:>10,} | {tiempo:>13.2f} | {tiempo_por_n2:>14.6f}")

    print("\n💡 Nota: Tiempo/n² debería ser relativamente constante (≈ 0.000001-0.000010)")
    print("   Si aumenta, confirma que es O(n²)")


if __name__ == "__main__":
    benchmark()
