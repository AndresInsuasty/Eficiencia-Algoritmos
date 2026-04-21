import time
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.numeros import es_par_impar

# Límite de 32 bits
INT32_MAX = 2**31 - 1


def measure_time_for_n_numbers(cantidad: int, repeticiones: int = 100) -> float:
    """
    Mide el tiempo total para evaluar es_par_impar en una cantidad de números.

    Args:
        cantidad: Cantidad de números a evaluar
        repeticiones: Cantidad de veces a repetir la operación para cada número

    Returns:
        Tiempo total en microsegundos
    """
    # Generar números aleatorios únicos en el rango de 32 bits
    numeros = [random.randint(1, INT32_MAX) for _ in range(cantidad)]

    inicio = time.perf_counter()
    for _ in range(repeticiones):
        for numero in numeros:
            es_par_impar(numero)
    fin = time.perf_counter()

    tiempo_total = fin - inicio
    # Tiempo total en microsegundos
    tiempo_microsegundos = tiempo_total * 1e6
    return tiempo_microsegundos


def benchmark():
    """
    Ejecuta el benchmark midiendo tiempo vs cantidad de números.
    """
    print("Iniciando benchmark de es_par_impar - Tiempo vs Cantidad de Números...")
    print(f"Rango de cantidad: 1 a 10,000 números")

    # Generar cantidades de números para evaluar (espaciadas logarítmicamente)
    cantidades = np.logspace(0, 4, 50, dtype=int)  # 1 a 10,000
    cantidades = sorted(list(set(cantidades)))  # Remover duplicados y ordenar

    tiempos = []

    print("\nMidiendo tiempos...")
    for i, cantidad in enumerate(cantidades):
        print(f"Progreso: {i+1}/{len(cantidades)} - Evaluando {cantidad:,} números", end="\r")
        tiempo_promedio = measure_time_for_n_numbers(cantidad, repeticiones=100)
        tiempos.append(tiempo_promedio)

    print("\n\nGenerando gráfica...")

    # Crear scatter plot
    plt.figure(figsize=(12, 7))
    plt.scatter(cantidades, tiempos, alpha=0.6, s=30, color='coral', edgecolors='darkred', linewidth=0.5)

    plt.xlabel('Cantidad de Números a Evaluar', fontsize=12, fontweight='bold')
    plt.ylabel('Tiempo Total (microsegundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: es_par_impar - Tiempo Total vs Cantidad de Números', fontsize=14, fontweight='bold')

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'es_par_impar_cantidad_benchmark.png')
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {img_path}")

    plt.show()

    # Mostrar estadísticas
    print("\n--- Estadísticas ---")
    print(f"Tiempo total mínimo: {min(tiempos):.4f} microsegundos")
    print(f"Tiempo total máximo: {max(tiempos):.4f} microsegundos")
    print(f"Tiempo total promedio: {np.mean(tiempos):.4f} microsegundos")

    # Mostrar algunos puntos de datos
    print("\n--- Muestra de Datos (Tiempo Total) ---")
    print("Cantidad  | Tiempo Total (µs) | Tiempo/Número (µs)")
    print("-" * 55)
    for cantidad, tiempo in zip(cantidades[::max(1, len(cantidades)//8)], tiempos[::max(1, len(cantidades)//8)]):
        tiempo_por_numero = tiempo / cantidad
        print(f"{cantidad:>8,} | {tiempo:>17.2f} | {tiempo_por_numero:>17.4f}")


if __name__ == "__main__":
    benchmark()
