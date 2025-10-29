"""
Juego del Dinosaurio de Chrome con IA Genetica
Version simplificada sin caracteres especiales
"""
import pygame
import sys
from game.simulation import Simulation
from utils.sprite_loader import initialize_sprites

# Constantes
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (247, 247, 247)


def main():
    """Funcion principal del juego."""
    # Inicializar Pygame
    pygame.init()
    
    # Crear ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Genetic AI - Aprendizaje por Algoritmo Genetico")
    
    # Reloj para controlar FPS
    clock = pygame.time.Clock()
    
    # Cargar sprites
    try:
        sprites = initialize_sprites()
        print("Sprites cargados correctamente")
    except Exception as e:
        print("Error al cargar sprites:", e)
        print("\nAsegurate de que 'sprites.png' esta en la raiz del proyecto.")
        pygame.quit()
        sys.exit(1)
    
    # Fuentes
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 20)
    
    # Crear simulacion
    simulation = Simulation()
    print("Simulacion iniciada")
    print("Poblacion:", len(simulation.dinos), "dinosaurios")
    print("\nLa evolucion ha comenzado!\n")
    
    # Control de tiempo para eventos periodicos
    tenth_counter = 0
    last_tenth_time = pygame.time.get_ticks()
    
    # Loop principal
    running = True
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Actualizar simulacion
        simulation.update()
        
        # Eventos periodicos (cada 50ms)
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
    print("\nHasta luego!")
    print("Ultima generacion alcanzada:", simulation.generation)
    print("Mejor score:", simulation.last_gen_max_score)


if __name__ == "__main__":
    main()