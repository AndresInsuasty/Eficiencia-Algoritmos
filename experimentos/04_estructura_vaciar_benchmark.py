import time
import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.estructuras import llenar_pila, llenar_cola, vaciar_pila, vaciar_cola


def measure_time_vaciar(cantidad: int, repeticiones: int = 100) -> dict[str, float]:
    """
    Mide el tiempo total para vaciar pilas y colas.

    Args:
        cantidad: Cantidad de elementos en la estructura
        repeticiones: Cantidad de veces a repetir la operación

    Returns:
        Diccionario con tiempos para pila y cola en microsegundos
    """
    # Medir pila
    inicio_pila = time.perf_counter()
    for _ in range(repeticiones):
        pila = llenar_pila(cantidad)
        vaciar_pila(pila)
    fin_pila = time.perf_counter()
    tiempo_pila = (fin_pila - inicio_pila) * 1e6

    # Medir cola
    inicio_cola = time.perf_counter()
    for _ in range(repeticiones):
        cola = llenar_cola(cantidad)
        vaciar_cola(cola)
    fin_cola = time.perf_counter()
    tiempo_cola = (fin_cola - inicio_cola) * 1e6

    return {"pila": tiempo_pila, "cola": tiempo_cola}


def benchmark():
    """
    Ejecuta el benchmark midiendo tiempo de vaciar pilas y colas vs cantidad de elementos.
    """
    print("Iniciando benchmark de vaciar Pila y Cola...")
    print(f"Rango de cantidad: 1 a 10,000 elementos")

    # Generar cantidades de elementos para evaluar
    cantidades = np.logspace(0, 4, 50, dtype=int)
    cantidades = sorted(list(set(cantidades)))

    tiempos_pila = []
    tiempos_cola = []

    print("\nMidiendo tiempos...")
    for i, cantidad in enumerate(cantidades):
        print(f"Progreso: {i+1}/{len(cantidades)} - Evaluando {cantidad:,} elementos", end="\r")
        tiempos = measure_time_vaciar(cantidad, repeticiones=100)
        tiempos_pila.append(tiempos["pila"])
        tiempos_cola.append(tiempos["cola"])

    print("\n\nGenerando gráfica...")

    # Crear scatter plot
    plt.figure(figsize=(12, 7))
    plt.scatter(cantidades, tiempos_pila, alpha=0.6, s=30, color='steelblue',
                edgecolors='navy', linewidth=0.5, label='Pila')
    plt.scatter(cantidades, tiempos_cola, alpha=0.6, s=30, color='coral',
                edgecolors='darkred', linewidth=0.5, label='Cola')

    plt.xlabel('Cantidad de Elementos', fontsize=12, fontweight='bold')
    plt.ylabel('Tiempo Total (microsegundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: Vaciar Pila vs Cola - Tiempo vs Cantidad de Elementos', fontsize=14, fontweight='bold')
    plt.legend()

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'estructura_vaciar_benchmark.png')
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {img_path}")

    plt.show()

    # Mostrar estadísticas
    print("\n--- Estadísticas Pila ---")
    print(f"Tiempo total mínimo: {min(tiempos_pila):.4f} microsegundos")
    print(f"Tiempo total máximo: {max(tiempos_pila):.4f} microsegundos")
    print(f"Tiempo total promedio: {np.mean(tiempos_pila):.4f} microsegundos")

    print("\n--- Estadísticas Cola ---")
    print(f"Tiempo total mínimo: {min(tiempos_cola):.4f} microsegundos")
    print(f"Tiempo total máximo: {max(tiempos_cola):.4f} microsegundos")
    print(f"Tiempo total promedio: {np.mean(tiempos_cola):.4f} microsegundos")

    # Mostrar algunos puntos de datos
    print("\n--- Muestra de Datos ---")
    print("Cantidad  | Tiempo Pila (µs) | Tiempo Cola (µs)")
    print("-" * 50)
    for cantidad, t_pila, t_cola in zip(cantidades[::max(1, len(cantidades)//8)],
                                         tiempos_pila[::max(1, len(cantidades)//8)],
                                         tiempos_cola[::max(1, len(cantidades)//8)]):
        print(f"{cantidad:>8,} | {t_pila:>16.2f} | {t_cola:>16.2f}")


if __name__ == "__main__":
    benchmark()
