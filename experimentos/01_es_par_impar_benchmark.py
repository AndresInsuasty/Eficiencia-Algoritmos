import time
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.numeros import es_par_impar

# Límite de 32 bits
INT32_MAX = 2**31 - 1

def measure_average_time(numero: int, repeticiones: int = 1000) -> float:
    """
    Mide el tiempo promedio de ejecución para evaluar es_par_impar.

    Args:
        numero: Número a evaluar
        repeticiones: Cantidad de veces a repetir la operación

    Returns:
        Tiempo promedio en microsegundos
    """
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        es_par_impar(numero)
    fin = time.perf_counter()

    tiempo_total = fin - inicio
    tiempo_promedio = (tiempo_total / repeticiones) * 1e6  # Convertir a microsegundos
    return tiempo_promedio


def generar_numeros_logspace(inicio: int = 1, fin: int = INT32_MAX, cantidad: int = 50) -> list[int]:
    """
    Genera números espaciados logarítmicamente entre inicio y fin.

    Args:
        inicio: Número inicial
        fin: Número final
        cantidad: Cantidad de puntos

    Returns:
        Lista de números enteros espaciados logarítmicamente
    """
    # Usamos logspace para generar puntos espaciados logarítmicamente
    log_space = np.logspace(np.log10(inicio), np.log10(fin), cantidad)
    return [int(x) for x in log_space]


def benchmark():
    """
    Ejecuta el benchmark y genera la gráfica.
    """
    print("Iniciando benchmark de es_par_impar...")
    print(f"Rango: 1 a {INT32_MAX:,}")

    # Generar números para evaluar
    numeros = generar_numeros_logspace(1, INT32_MAX, cantidad=50)

    tiempos = []

    print("\nMidiendo tiempos...")
    for i, numero in enumerate(numeros):
        print(f"Progreso: {i+1}/{len(numeros)} - Evaluando número: {numero:,}", end="\r")
        tiempo_promedio = measure_average_time(numero, repeticiones=1000)
        tiempos.append(tiempo_promedio)

    print("\n\nGenerando gráfica...")

    # Crear scatter plot
    plt.figure(figsize=(12, 7))
    plt.scatter(numeros, tiempos, alpha=0.6, s=30, color='steelblue', edgecolors='navy', linewidth=0.5)

    plt.xlabel('Número', fontsize=12, fontweight='bold')
    plt.ylabel('Tiempo Promedio de Ejecución (microsegundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: es_par_impar - Tiempo vs Número', fontsize=14, fontweight='bold')

    # Usar escala logarítmica para el eje X (para mejor visualización)
    plt.xscale('log')

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'es_par_impar_benchmark.png')
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {img_path}")

    plt.show()

    # Mostrar estadísticas
    print("\n--- Estadísticas ---")
    print(f"Tiempo promedio mínimo: {min(tiempos):.4f} microsegundos")
    print(f"Tiempo promedio máximo: {max(tiempos):.4f} microsegundos")
    print(f"Tiempo promedio medio: {np.mean(tiempos):.4f} microsegundos")
    print(f"Desviación estándar: {np.std(tiempos):.4f} microsegundos")


if __name__ == "__main__":
    benchmark()
