import time
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.ordenamiento import bubble_sort, merge_sort


def medir_tiempo_algoritmo(algoritmo, arreglo: list, repeticiones: int = 3) -> float:
    """Mide el tiempo de ejecución de un algoritmo de ordenamiento."""
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        algoritmo(arreglo)
    fin = time.perf_counter()
    return (fin - inicio) * 1e6


def benchmark():
    """Compara Bubble Sort (O(n²)) vs Merge Sort (O(n log n))."""
    print("Iniciando benchmark comparativo: Bubble Sort vs Merge Sort...")
    print(f"Rango de tamaño: 50 a 2,000 elementos\n")

    # Generar tamaños
    tamaños = np.logspace(1.7, 3.3, 30, dtype=int)
    tamaños = sorted(list(set(tamaños)))

    tiempos_bubble = []
    tiempos_merge = []

    print("Midiendo tiempos...")
    for i, tamaño in enumerate(tamaños):
        print(f"Progreso: {i+1}/{len(tamaños)} - Tamaño: {tamaño:,} elementos", end="\r")

        arreglo = [random.randint(1, 10000) for _ in range(tamaño)]

        # Medir Bubble Sort
        tiempo_bubble = medir_tiempo_algoritmo(bubble_sort, arreglo, repeticiones=2)
        tiempos_bubble.append(tiempo_bubble)

        # Medir Merge Sort
        tiempo_merge = medir_tiempo_algoritmo(merge_sort, arreglo, repeticiones=2)
        tiempos_merge.append(tiempo_merge)

    print("\n\nGenerando gráfica...")

    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Subplot 1: Comparación directa (escala lineal)
    ax1.scatter(tamaños, tiempos_bubble, alpha=0.7, s=50, color='#FF6B6B',
                label='Bubble Sort O(n²)', edgecolors='darkred', linewidth=1)
    ax1.scatter(tamaños, tiempos_merge, alpha=0.7, s=50, color='#4ECDC4',
                label='Merge Sort O(n log n)', edgecolors='darkblue', linewidth=1)

    ax1.set_xlabel('Tamaño del Arreglo (n)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Tiempo Total (microsegundos)', fontsize=12, fontweight='bold')
    ax1.set_title('Comparación: Bubble Sort vs Merge Sort', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=11, loc='upper left')
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Subplot 2: Escala logarítmica para mejor visualización
    ax2.scatter(tamaños, tiempos_bubble, alpha=0.7, s=50, color='#FF6B6B',
                label='Bubble Sort O(n²)', edgecolors='darkred', linewidth=1)
    ax2.scatter(tamaños, tiempos_merge, alpha=0.7, s=50, color='#4ECDC4',
                label='Merge Sort O(n log n)', edgecolors='darkblue', linewidth=1)

    ax2.set_xlabel('Tamaño del Arreglo (n)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Tiempo Total (microsegundos)', fontsize=12, fontweight='bold')
    ax2.set_title('Escala Logarítmica (eje Y)', fontsize=13, fontweight='bold')
    ax2.set_yscale('log')
    ax2.legend(fontsize=11, loc='upper left')
    ax2.grid(True, alpha=0.3, linestyle='--', which='both')

    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'bubble_vs_merge_benchmark.png')
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {img_path}")

    plt.show()

    # Mostrar estadísticas
    print("\n--- Estadísticas ---")
    print(f"Bubble Sort:  mín={min(tiempos_bubble):.2f}µs, máx={max(tiempos_bubble):.2f}µs")
    print(f"Merge Sort:   mín={min(tiempos_merge):.2f}µs, máx={max(tiempos_merge):.2f}µs")

    # Comparar ratios
    print("\n--- Ratio de Tiempo (Bubble / Merge) ---")
    print("Tamaño (n) | Bubble (µs)  | Merge (µs)   | Ratio")
    print("-" * 60)
    for tamaño, tb, tm in zip(tamaños[::max(1, len(tamaños)//8)],
                              tiempos_bubble[::max(1, len(tamaños)//8)],
                              tiempos_merge[::max(1, len(tamaños)//8)]):
        ratio = tb / tm if tm > 0 else 0
        print(f"{tamaño:>10,} | {tb:>12.2f} | {tm:>12.2f} | {ratio:>6.1f}x")

    print("\n💡 Nota: El ratio aumenta dramáticamente (Bubble es MUCHO más lento)")


if __name__ == "__main__":
    benchmark()
