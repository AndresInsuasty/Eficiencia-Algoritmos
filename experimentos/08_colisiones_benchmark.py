import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import random

# Agregar carpeta padre al path para importar algoritmos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algoritmos.geometria import Circulo, Punto, obtener_pares_colisionados


class CirculoEnSimulacion:
    """Círculo que se mueve en la simulación."""

    def __init__(self, x: float, y: float, radio: float, ancho: int, alto: int):
        self.circulo = Circulo(Punto(x, y), radio)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.ancho = ancho
        self.alto = alto

    def actualizar(self):
        """Actualiza la posición y maneja rebotes."""
        self.circulo.centro.x += self.vx
        self.circulo.centro.y += self.vy

        # Rebotar en bordes
        if self.circulo.centro.x - self.circulo.radio < 0 or \
           self.circulo.centro.x + self.circulo.radio > self.ancho:
            self.vx *= -1

        if self.circulo.centro.y - self.circulo.radio < 0 or \
           self.circulo.centro.y + self.circulo.radio > self.alto:
            self.vy *= -1

        # Mantener dentro de límites
        self.circulo.centro.x = max(self.circulo.radio,
                                     min(self.ancho - self.circulo.radio,
                                         self.circulo.centro.x))
        self.circulo.centro.y = max(self.circulo.radio,
                                     min(self.alto - self.circulo.radio,
                                         self.circulo.centro.y))

    def rebotar_con(self, otro: 'CirculoEnSimulacion'):
        """Calcula el rebote elástico con otro círculo."""
        dx = otro.circulo.centro.x - self.circulo.centro.x
        dy = otro.circulo.centro.y - self.circulo.centro.y
        distancia = (dx**2 + dy**2)**0.5

        if distancia == 0:
            return

        nx = dx / distancia
        ny = dy / distancia

        dvx = otro.vx - self.vx
        dvy = otro.vy - self.vy
        dvn = dvx * nx + dvy * ny

        if dvn >= 0:
            return

        self.vx += dvn * nx
        self.vy += dvn * ny
        otro.vx -= dvn * nx
        otro.vy -= dvn * ny

        min_dist = self.circulo.radio + otro.circulo.radio
        solapamiento = min_dist - distancia
        if solapamiento > 0:
            separacion = solapamiento / 2 + 0.5
            self.circulo.centro.x -= separacion * nx
            self.circulo.centro.y -= separacion * ny
            otro.circulo.centro.x += separacion * nx
            otro.circulo.centro.y += separacion * ny


def simular_colisiones(cantidad_circulos: int, duracion_segundos: int = 20, fps: int = 60) -> int:
    """
    Simula círculos colisionando durante un tiempo determinado.

    Args:
        cantidad_circulos: Cantidad de círculos en la simulación
        duracion_segundos: Duración de la simulación en segundos
        fps: Fotogramas por segundo

    Returns:
        Total de colisiones detectadas acumuladas
    """
    ancho, alto = 1000, 700
    circulos = []

    # Crear círculos aleatorios
    random.seed(42)
    for _ in range(cantidad_circulos):
        x = random.uniform(50, ancho - 50)
        y = random.uniform(50, alto - 50)
        radio = random.uniform(15, 30)
        circulos.append(CirculoEnSimulacion(x, y, radio, ancho, alto))

    total_colisiones = 0
    frames_totales = duracion_segundos * fps

    # Simular
    for _ in range(frames_totales):
        # Actualizar posiciones
        for circulo in circulos:
            circulo.actualizar()

        # Detectar colisiones
        circulos_geo = [c.circulo for c in circulos]
        pares_colisionados = obtener_pares_colisionados(circulos_geo)

        # Acumular colisiones
        total_colisiones += len(pares_colisionados)

        # Aplicar rebotes
        for i, j in pares_colisionados:
            circulos[i].rebotar_con(circulos[j])

    return total_colisiones


def benchmark():
    """Ejecuta el benchmark midiendo colisiones vs cantidad de círculos."""
    print("Iniciando benchmark de Colisiones...")
    print("Duración por simulación: 20 segundos")
    print(f"Rango de círculos: 10 a 200\n")

    # Generar cantidades de círculos
    cantidades = np.linspace(10, 200, 20, dtype=int)

    colisiones = []

    print("Midiendo colisiones (esto puede tomar algunos minutos)...")
    for i, cantidad in enumerate(cantidades):
        print(f"Progreso: {i+1}/{len(cantidades)} - Cantidad: {cantidad:,} círculos", end="\r")
        total = simular_colisiones(cantidad, duracion_segundos=20)
        colisiones.append(total)

    print("\n\nGenerando gráfica...")

    # Crear scatter plot
    plt.figure(figsize=(12, 7))
    plt.scatter(cantidades, colisiones, alpha=0.7, s=80, color='#F39C12',
                edgecolors='#D68910', linewidth=2)

    # Línea de tendencia para visualizar el crecimiento
    z = np.polyfit(cantidades, colisiones, 2)
    p = np.poly1d(z)
    plt.plot(cantidades, p(cantidades), "r--", alpha=0.6, linewidth=2, label='Tendencia')

    plt.xlabel('Cantidad de Círculos (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Colisiones Acumuladas (20 segundos)', fontsize=12, fontweight='bold')
    plt.title('Benchmark: Colisiones en Simulación de 20 Segundos', fontsize=14, fontweight='bold')

    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=11)
    plt.tight_layout()

    # Guardar figura
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'colisiones_benchmark.png')
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    plt.savefig(img_path, dpi=300, bbox_inches='tight')
    print(f"Gráfica guardada en: {img_path}")

    plt.show()

    # Mostrar estadísticas
    print("\n--- Estadísticas ---")
    print(f"Mínimo de colisiones: {min(colisiones):,}")
    print(f"Máximo de colisiones: {max(colisiones):,}")

    # Mostrar algunos puntos de datos
    print("\n--- Muestra de Datos ---")
    print("Círculos | Colisiones (20s) | Colisiones/Círculo")
    print("-" * 55)
    for cantidad, col in zip(cantidades[::max(1, len(cantidades)//8)],
                             colisiones[::max(1, len(cantidades)//8)]):
        col_por_circulo = col / cantidad
        print(f"{cantidad:>8} | {col:>16,} | {col_por_circulo:>18.0f}")

    print("\n💡 Observaciones:")
    print("   • Más círculos = Más colisiones posibles")
    print("   • Crecimiento es cuadrático (relación con O(n²))")
    print("   • Con n círculos: ~n² comparaciones por frame")


if __name__ == "__main__":
    benchmark()
