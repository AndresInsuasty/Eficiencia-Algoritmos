import requests
import time
import numpy as np
import matplotlib.pyplot as plt
import os


def fetch_dog_image_time() -> float:
    """
    Descarga una imagen de perro y retorna el tiempo de respuesta.

    Returns:
        float: Tiempo de respuesta en segundos
    """
    start_time = time.perf_counter()

    try:
        response = requests.get(
            "https://dog.ceo/api/breeds/image/random",
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        if data["status"] == "success":
            end_time = time.perf_counter()
            return end_time - start_time
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def benchmark_dog_api(num_calls: int = 10) -> tuple[list[float], float, float]:
    """
    Realiza múltiples llamadas a la API y retorna los tiempos.

    Args:
        num_calls: Número de llamadas a realizar

    Returns:
        tuple: (lista de tiempos, media, desviación estándar)
    """
    times = []

    print(f"Ejecutando {num_calls} llamadas a la API...")
    for i in range(num_calls):
        response_time = fetch_dog_image_time()
        if response_time is not None:
            times.append(response_time)
            print(f"  [{i+1}/{num_calls}] {response_time:.4f}s ({response_time*1000:.2f}ms)")
        else:
            print(f"  [{i+1}/{num_calls}] Error en la llamada")

    # Calcular estadísticas
    times = np.array(times)
    mean_time = np.mean(times)
    std_time = np.std(times)

    print(f"\n[ESTADISTICAS]")
    print(f"  Media: {mean_time:.4f}s ({mean_time*1000:.2f}ms)")
    print(f"  Desviacion estandar: {std_time:.4f}s ({std_time*1000:.2f}ms)")
    print(f"  Minimo: {np.min(times):.4f}s ({np.min(times)*1000:.2f}ms)")
    print(f"  Maximo: {np.max(times):.4f}s ({np.max(times)*1000:.2f}ms)")

    return times, mean_time, std_time


def plot_benchmark_results(times: np.ndarray, mean_time: float, std_time: float):
    """
    Grafica los resultados del benchmark.

    Args:
        times: Array de tiempos de respuesta
        mean_time: Tiempo medio
        std_time: Desviación estándar
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot de los tiempos
    x_values = np.arange(1, len(times) + 1)
    ax.scatter(x_values, times * 1000, s=100, alpha=0.6, color='steelblue', label='Tiempos de respuesta')

    # Línea de media
    ax.axhline(y=mean_time * 1000, color='green', linestyle='-', linewidth=2, label=f'Media: {mean_time*1000:.2f}ms')

    # Banda de desviación estándar
    upper_bound = (mean_time + std_time) * 1000
    lower_bound = (mean_time - std_time) * 1000
    ax.axhline(y=upper_bound, color='orange', linestyle='--', linewidth=1.5, label=f'±1σ: {std_time*1000:.2f}ms')
    ax.axhline(y=lower_bound, color='orange', linestyle='--', linewidth=1.5)
    ax.fill_between(x_values, lower_bound, upper_bound, alpha=0.2, color='orange')

    ax.set_xlabel('Número de llamada', fontsize=12)
    ax.set_ylabel('Tiempo de respuesta (ms)', fontsize=12)
    ax.set_title('Dog API - Benchmark de Tiempos de Respuesta (10 llamadas)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)

    # Guardar figura
    output_path = os.path.join(os.path.dirname(__file__), 'img', 'dog_image_benchmark.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n[GRAFICO GUARDADO] {output_path}")

    plt.show()


if __name__ == "__main__":
    times, mean_time, std_time = benchmark_dog_api(num_calls=10)
    plot_benchmark_results(times, mean_time, std_time)
