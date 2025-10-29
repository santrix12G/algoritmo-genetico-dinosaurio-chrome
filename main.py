"""
Juego del Dinosaurio de Chrome con IA Genética
Archivo principal - Ejecutar este archivo para iniciar la simulación
"""
# -*- coding: utf-8 -*-
import pygame
import sys
import os


scores=[]
best_weights={}

# Configurar encoding para Windows
if os.name == 'nt':  # Windows
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from game.simulation import Simulation
from utils.sprite_loader import initialize_sprites


# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (247, 247, 247)
simulation=None

def grafica():
    # === 📊 Generar gráficas después de la simulación ===
    print(simulation.generation_data)
    if simulation.generation_data:
        import matplotlib.pyplot as plt
        import numpy as np

        data = np.array(simulation.generation_data)
        generations = data[:, 0]
        max_scores = data[:, 1]
        avg_scores = data[:, 2]
        min_scores = data[:, 3]

        plt.figure(figsize=(10, 6))
        plt.plot(generations, avg_scores, 'b-', label='Score Promedio', linewidth=2)
        plt.plot(generations, max_scores, 'r-', label='Score Máximo', linewidth=2)
        plt.plot(generations, min_scores, 'y-', label='Score Mínimo', linewidth=1.5, alpha=0.6)

        plt.xlabel("Generación")
        plt.ylabel("Score")
        plt.title("📈 Evolución del Score por Generación")
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

        # === 📊 Diversidad genética ===
        if data.shape[1] >= 6:  # Si se guardó varianza
            diversity = data[:, 5]
            plt.figure(figsize=(10, 5))
            plt.plot(generations, diversity, color='purple', linewidth=2)
            plt.title("🌿 Diversidad Genética (Desviación estándar del fitness)")
            plt.xlabel("Generación")
            plt.ylabel("Desviación estándar")
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.show()



def main():
    global simulation
    """Función principal del juego."""
    # Inicializar Pygame
    pygame.init()
    
    # Crear ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Genetic AI - Aprendizaje por Algoritmo Genético")
    
    # Reloj para controlar FPS
    clock = pygame.time.Clock()
    
    # Cargar sprites
    try:
        sprites = initialize_sprites()
        print("OK - Sprites cargados correctamente")
    except Exception as e:
        print(f"ERROR - Error al cargar sprites: {e}")
        print("\nAsegurate de que 'sprites.png' esta en la raiz del proyecto.")
        pygame.quit()
        sys.exit(1)
    
    # Fuentes
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 20)
    
    # Crear simulación
    simulation = Simulation()
    print("OK - Simulacion iniciada")
    print(f"OK - Poblacion: {len(simulation.dinos)} dinosaurios")
    print("\nLa evolucion ha comenzado!\n")
    
    # Control de tiempo para eventos periódicos
    tenth_counter = 0
    last_tenth_time = pygame.time.get_ticks()
    
    # Loop principal
    running = True
    while running and simulation.generation<=30:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Actualizar simulación
        simulation.update()        
        # Eventos periódicos (cada 50ms)
        current_time = pygame.time.get_ticks()
        if current_time - last_tenth_time > 50:
            last_tenth_time = current_time
            tenth_counter += 1
            
            # Cada 0.1 segundos
            if tenth_counter % 2 == 0:
                simulation.tenth_of_second()
            
            # Cada 0.25 segundos
            if tenth_counter % 5 == 0:
                simulation.quarter_of_second()
        
        # Dibujar todo
        screen.fill(BACKGROUND_COLOR)
        simulation.draw(screen, sprites, font, small_font)
        
        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)
    
    # Limpiar y salir
    pygame.quit()
    grafica()
    print("\nHasta luego!")
    print(f"Ultima generacion alcanzada: {simulation.generation}")
    print(f"Mejor score: {simulation.last_gen_max_score}")


if __name__ == "__main__":
    main()