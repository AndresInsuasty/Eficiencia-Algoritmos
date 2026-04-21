import time
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.pares import contar_inversiones


def medir_tiempo_inversiones(tamaño: int, repeticiones: int = 5) -> float:
    """
    Mide el tiempo total para contar inversiones en un arreglo.

    Args:
        tamaño: Cantidad de números en el arreglo
        repeticiones: Veces a repetir la operación

    Returns:
        Tiempo total en microsegundos
    """
    arreglo = [random.randint(1, 10000) for _ in range(tamaño)]

    inicio = time.perf_counter()
    for _ in range(repeticiones):
        contar_inversiones(arreglo)
    fin = time.perf_counter()

    return (fin - inicio) * 1e6


def benchmark():
    """Ejecuta el benchmark midiendo tiempo vs tamaño del arreglo."""
    print("Iniciando benchmark de Contador de Inversiones...")
    print("Complejidad: O(n²)")
    print(f"Rango de tamaño: 50 a 1,500 elementos\n")

    # Generar tamaños de arreglos
    tamaños = np.logspace(1.7, 3.17, 30, dtype=int)
    tamaños = sorted(list(set(tamaños)))

    tiempos = []

    print("Midiendo tiempos...")
    for i, tamaño in enumerate(tamaños):
        print(f"Progreso: {i+1}/{len(tamaños)} - Tamaño: {tamaño:,} elementos", end="\r")
        tiempo = medir_tiempo_inversiones(tamaño, repeticiones=3)
        tiempos.append(tiempo)

    print("\n\nGenerando gráfica...")

    # Crear scatter plot
    plt.figure(figsize=(12, 7))
    plt.scatter(tamaños, tiempos, alpha=0.7, s=50, color='#9B59B6', edgecolors='#6C3483', linewidth=1)

    plt.xlabel('Tamaño del Arreglo (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Tiempo Total (microsegundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: Contador de Inversiones - Complejidad O(n²)', fontsize=14, fontweight='bold')

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'contador_inversiones_benchmark.png')
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
    print("Tamaño (n) | Tiempo (µs)   | Tiempo/n² (µs)  | Comparaciones")
    print("-" * 70)
    for tamaño, tiempo in zip(tamaños[::max(1, len(tamaños)//8)], tiempos[::max(1, len(tamaños)//8)]):
        tiempo_por_n2 = tiempo / (tamaño ** 2)
        comparaciones = (tamaño * (tamaño - 1)) // 2
        print(f"{tamaño:>10,} | {tiempo:>13.2f} | {tiempo_por_n2:>15.6f} | {comparaciones:>12,}")

    print("\n💡 Explicación:")
    print("   - Cada arreglo de tamaño n requiere ~n(n-1)/2 comparaciones")
    print("   - Esto es exactamente O(n²)")
    print("   - Tiempo/n² debería ser relativamente constante")


if __name__ == "__main__":
    benchmark()
