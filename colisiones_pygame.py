#!/usr/bin/env python3
"""
DETECCIÓN DE COLISIONES - Pygame Interactive Demo

Visualización interactiva en tiempo real con Pygame.
Muestra claramente cómo O(n²) impacta el rendimiento.
"""

import sys
import os
import pygame
import random
import time
from typing import List, Tuple

# Agregar carpeta padre al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algoritmos.geometria import Circulo, Punto, obtener_pares_colisionados


class CirculoAnimado:
    """Círculo que se mueve en la pantalla."""

    def __init__(self, x: float, y: float, radio: float, pantalla_ancho: int, pantalla_alto: int):
        self.circulo = Circulo(Punto(x, y), radio)
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.pantalla_ancho = pantalla_ancho
        self.pantalla_alto = pantalla_alto
        self.en_colision = False

    def actualizar(self):
        """Actualiza la posición y maneja rebotes."""
        self.circulo.centro.x += self.vx
        self.circulo.centro.y += self.vy

        # Rebotar en bordes
        if self.circulo.centro.x - self.circulo.radio < 0 or \
           self.circulo.centro.x + self.circulo.radio > self.pantalla_ancho:
            self.vx *= -1

        if self.circulo.centro.y - self.circulo.radio < 0 or \
           self.circulo.centro.y + self.circulo.radio > self.pantalla_alto:
            self.vy *= -1

        # Mantener dentro de límites
        self.circulo.centro.x = max(self.circulo.radio,
                                     min(self.pantalla_ancho - self.circulo.radio,
                                         self.circulo.centro.x))
        self.circulo.centro.y = max(self.circulo.radio,
                                     min(self.pantalla_alto - self.circulo.radio,
                                         self.circulo.centro.y))

    def rebotar_con(self, otro: 'CirculoAnimado'):
        """Calcula el rebote elástico con otro círculo."""
        # Vector entre centros
        dx = otro.circulo.centro.x - self.circulo.centro.x
        dy = otro.circulo.centro.y - self.circulo.centro.y
        distancia = (dx**2 + dy**2)**0.5

        if distancia == 0:
            return

        # Normalizar
        nx = dx / distancia
        ny = dy / distancia

        # Velocidad relativa
        dvx = otro.vx - self.vx
        dvy = otro.vy - self.vy

        # Velocidad relativa en dirección de colisión
        dvn = dvx * nx + dvy * ny

        # No hacer nada si se están alejando
        if dvn >= 0:
            return

        # Intercambiar velocidades en dirección de colisión (colisión elástica 1D simplificada)
        self.vx += dvn * nx
        self.vy += dvn * ny
        otro.vx -= dvn * nx
        otro.vy -= dvn * ny

        # Separar círculos para evitar penetración
        min_dist = self.circulo.radio + otro.circulo.radio
        solapamiento = min_dist - distancia
        if solapamiento > 0:
            separacion = solapamiento / 2 + 0.5
            self.circulo.centro.x -= separacion * nx
            self.circulo.centro.y -= separacion * ny
            otro.circulo.centro.x += separacion * nx
            otro.circulo.centro.y += separacion * ny

    def dibujar(self, pantalla: pygame.Surface):
        """Dibuja el círculo en la pantalla."""
        color = (255, 100, 100) if self.en_colision else (78, 205, 196)  # Rojo si colisiona, azul si no
        pygame.draw.circle(pantalla, color,
                          (int(self.circulo.centro.x), int(self.circulo.centro.y)),
                          int(self.circulo.radio), 2)
        pygame.draw.circle(pantalla, color,
                          (int(self.circulo.centro.x), int(self.circulo.centro.y)),
                          int(self.circulo.radio))


class SimuladorPygame:
    """Simulador principal con Pygame."""

    def __init__(self, num_circulos: int = 15):
        pygame.init()

        self.pantalla_ancho = 1200
        self.pantalla_alto = 700
        self.pantalla = pygame.display.set_mode((self.pantalla_ancho, self.pantalla_alto))
        pygame.display.set_caption('Detección de Colisiones - O(n²)')

        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_grande = pygame.font.Font(None, 36)

        # Crear círculos
        self.circulos_animados: List[CirculoAnimado] = []
        self.num_circulos = num_circulos
        random.seed(42)

        for _ in range(num_circulos):
            x = random.uniform(50, self.pantalla_ancho - 50)
            y = random.uniform(50, self.pantalla_alto - 50)
            radio = random.uniform(15, 30)
            self.circulos_animados.append(
                CirculoAnimado(x, y, radio, self.pantalla_ancho, self.pantalla_alto)
            )

        # Estadísticas
        self.pares_colisionados: List[Tuple[int, int]] = []
        self.comparaciones_totales = 0
        self.fps = 0
        self.tiempo_deteccion = 0
        self.paused = False
        self.mostrar_lineas = True
        self.colisiones_acumuladas = 0

    def actualizar(self):
        """Actualiza el estado de la simulación."""
        if not self.paused:
            for circulo in self.circulos_animados:
                circulo.actualizar()

        # Detectar colisiones (operación O(n²))
        inicio = time.perf_counter()

        # Obtener lista de círculos para detección
        circulos_geo = [c.circulo for c in self.circulos_animados]
        self.pares_colisionados = obtener_pares_colisionados(circulos_geo)
        self.comparaciones_totales = (len(circulos_geo) * (len(circulos_geo) - 1)) // 2

        # Acumular colisiones
        self.colisiones_acumuladas += len(self.pares_colisionados)

        # Aplicar rebotes físicos
        for i, j in self.pares_colisionados:
            self.circulos_animados[i].rebotar_con(self.circulos_animados[j])

        fin = time.perf_counter()
        self.tiempo_deteccion = (fin - inicio) * 1000  # En millisegundos

        # Actualizar estado de colisión
        for i, circulo in enumerate(self.circulos_animados):
            circulo.en_colision = any(i in par for par in self.pares_colisionados)

        # FPS
        self.fps = self.reloj.get_fps()

    def dibujar(self):
        """Dibuja todo en la pantalla."""
        self.pantalla.fill((30, 30, 40))

        # Dibujar círculos
        for circulo in self.circulos_animados:
            circulo.dibujar(self.pantalla)

        # Dibujar líneas de colisión
        if self.mostrar_lineas:
            for i, j in self.pares_colisionados:
                c1 = self.circulos_animados[i].circulo
                c2 = self.circulos_animados[j].circulo
                pygame.draw.line(self.pantalla, (200, 50, 50),
                               (int(c1.centro.x), int(c1.centro.y)),
                               (int(c2.centro.x), int(c2.centro.y)), 2)

        # Panel de información (lado derecho)
        self._dibujar_panel_info()

        # Instrucciones
        self._dibujar_instrucciones()

        pygame.display.flip()

    def _dibujar_panel_info(self):
        """Dibuja el panel de información."""
        panel_ancho = 250
        panel_x = self.pantalla_ancho - panel_ancho - 10
        panel_y = 10

        # Fondo del panel
        pygame.draw.rect(self.pantalla, (50, 50, 70),
                        (panel_x - 5, panel_y - 5, panel_ancho + 10, 150))
        pygame.draw.rect(self.pantalla, (100, 100, 130),
                        (panel_x - 5, panel_y - 5, panel_ancho + 10, 150), 2)

        y = panel_y + 10

        # Título
        titulo = self.fuente_grande.render("ESTADÍSTICAS", True, (78, 205, 196))
        self.pantalla.blit(titulo, (panel_x, y))
        y += 40

        # Información simplificada
        info = [
            f"Círculos: {self.num_circulos}",
            f"",
            f"Colisiones: {self.colisiones_acumuladas:,}",
        ]

        for linea in info:
            if linea:
                texto = self.fuente.render(linea, True, (200, 200, 200))
                self.pantalla.blit(texto, (panel_x + 10, y))
            y += 35

    def _dibujar_instrucciones(self):
        """Dibuja las instrucciones."""
        instrucciones = [
            "CONTROLES:",
            "ESPACIO - Pausa/Reanuda",
            "L - Mostrar/Ocultar líneas",
            "+ - Más círculos",
            "- - Menos círculos",
            "R - Reset",
            "ESC - Salir",
        ]

        y = 10
        for instruccion in instrucciones:
            if instruccion == "CONTROLES:":
                texto = self.fuente_grande.render(instruccion, True, (78, 205, 196))
            else:
                texto = self.fuente.render(instruccion, True, (200, 200, 200))
            self.pantalla.blit(texto, (10, y))
            y += 25

    def manejar_eventos(self) -> bool:
        """Maneja eventos del teclado. Retorna False si debe cerrar."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif evento.key == pygame.K_l:
                    self.mostrar_lineas = not self.mostrar_lineas
                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_EQUALS:
                    if self.num_circulos < 100:
                        self.num_circulos += 1
                        x = random.uniform(50, self.pantalla_ancho - 50)
                        y = random.uniform(50, self.pantalla_alto - 50)
                        radio = random.uniform(15, 30)
                        self.circulos_animados.append(
                            CirculoAnimado(x, y, radio, self.pantalla_ancho, self.pantalla_alto)
                        )
                elif evento.key == pygame.K_MINUS:
                    if self.num_circulos > 1:
                        self.num_circulos -= 1
                        self.circulos_animados.pop()
                elif evento.key == pygame.K_r:
                    num_temp = self.num_circulos
                    self.__init__(num_temp)

        return True

    def ejecutar(self):
        """Loop principal."""
        ejecutando = True

        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(60)  # 60 FPS

        pygame.quit()


def main():
    """Función principal."""
    print("\n" + "=" * 70)
    print("🎮 DETECCIÓN DE COLISIONES CON PYGAME")
    print("=" * 70)
    print("\nIniciando simulación interactiva...")
    print("\nControles:")
    print("  ESPACIO  - Pausa/Reanuda")
    print("  L        - Mostrar/Ocultar líneas de colisión")
    print("  +/-      - Agregar/Quitar círculos")
    print("  R        - Reset")
    print("  ESC      - Salir")
    print("\n" + "=" * 70 + "\n")

    simulador = SimuladorPygame(num_circulos=15)
    simulador.ejecutar()

    print("\n¡Simulación finalizada!")


if __name__ == "__main__":
    # Verificar si pygame está instalado
    try:
        import pygame
    except ImportError:
        print("\n❌ Error: Pygame no está instalado")
        print("\nInstala con:")
        print("  pip install pygame")
        sys.exit(1)

    main()
