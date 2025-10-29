"""
Simulación principal del juego con algoritmo genético.
"""
import random
import pygame
from game.dino import Dino
from game.enemy import Cactus, Bird
from game.game_object import Ground
import numpy as np


# Constantes
DINOS_PER_GENERATION = 500
MIN_SPAWN_MILLIS = 1000
MAX_SPAWN_MILLIS = 3000


class Simulation:
    """
    Gestiona la simulación completa del juego:
    - Población de dinosaurios
    - Enemigos
    - Física y colisiones
    - Algoritmo genético
    """
    
    def __init__(self):
        # Crear población inicial
        self.dinos = [Dino() for _ in range(DINOS_PER_GENERATION)]
        self.enemies = []
        self.generation_data = []
        
        # Estado del juego
        self.speed = 10
        self.ground = Ground()
        self.score = 0
        self.generation = 1
        self.last_gen_avg_score = 0
        self.last_gen_max_score = 0
        self.dinos_alive = DINOS_PER_GENERATION
        self.best_weights=None
        self.best_dino_alive=None
        self.best_score_dino=0
        
        # Control de spawn de enemigos
        self.last_spawn_time = pygame.time.get_ticks()
        self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
    
    def update(self):
        """Actualiza toda la simulación en cada frame."""
        # Actualizar dinosaurios vivos
        for dino in self.dinos:
            if dino.alive:
                dino.update(self.next_obstacle_info(dino), int(self.speed))
        
        # Actualizar enemigos
        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.update(int(self.speed))
            if enemy.is_offscreen():
                enemies_to_remove.append(enemy)
        
        # Remover enemigos fuera de pantalla
        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
        
        # Spawn de nuevos enemigos
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.time_to_spawn:
            self.spawn_enemy()
            self.last_spawn_time = current_time
            self.time_to_spawn = random.uniform(MIN_SPAWN_MILLIS, MAX_SPAWN_MILLIS)
        
        # Verificar colisiones
        self.check_collisions()
        
        # Actualizar suelo y velocidad
        self.ground.update(int(self.speed))
        self.speed += 0.001
    
    
    def check_collisions(self):
        """Verifica colisiones entre dinosaurios y enemigos."""
        self.dinos_alive = 0
        
        for dino in self.dinos:
            if dino.alive:
                for enemy in self.enemies:
                    if dino.is_collisioning_with(enemy):
                        dino.die(self.score)
                        break
                
                if dino.alive:
                    self.dinos_alive += 1
        
        # Si todos murieron, nueva generación
        if self.dinos_alive == 0:
            self.next_generation()
    
    

    def next_generation(self):
        """
        Crea la siguiente generación usando algoritmo genético:
        - 5% mejores sin cambios
        - 5% completamente nuevos
        - 30% mutaciones del mejor
        - 40% mutaciones del top 5%
        - 20% crossover del top 5%
        """
        self.score = 0
        self.generation += 1
        self.speed = 15
        self.enemies.clear()
        
        # Calcular estadísticas
        dinos_score_sum = sum(dino.score for dino in self.dinos)
        max_score=0
        min_score=1e18
        suma=0
        values=[]
        for dino in self.dinos:
            max_score=max(max_score,dino.score)
            min_score=min(min_score,dino.score)
            suma+=dino.score
            values.append(dino.score)
        avg_score=suma/len(self.dinos)
        varianza=np.var(values)
        desviacion=np.std(values)
        self.generation_data.append([self.generation-1, max_score, avg_score, min_score,varianza,desviacion])
        

            
        self.last_gen_avg_score = dinos_score_sum // DINOS_PER_GENERATION
        
        # Ordenar por score (mejor a peor)
        self.dinos.sort(reverse=True)
        self.last_gen_max_score = self.dinos[0].score

        if self.best_score_dino<self.last_gen_max_score:
            self.best_dino_alive=self.dinos[0]
            self.best_score_dino=self.dinos[0].score
        
        # Crear nueva generación
        new_dinos = []
        new_dinos.append(self.best_dino_alive)
        top_5_percent = int(DINOS_PER_GENERATION * 0.05)
        
        # 5% mejores sin cambios
        for i in range(top_5_percent):
            self.dinos[i].reset()
            new_dinos.append(self.dinos[i])
        
        # 5% completamente nuevos
        for _ in range(top_5_percent):
            new_dinos.append(Dino())
        
        # 30% mutaciones del mejor
        for _ in range(int(DINOS_PER_GENERATION * 0.3)):
            #Seleccion por torneo
            # candidates = random.sample(self.dinos, 5)
            # father=max(candidates, key=lambda d: d.score)
            father=self.dinos[0]
            son = Dino()
            son.genome = father.genome.mutate()
            son.init_brain()
            new_dinos.append(son)
        
        # 40% mutaciones del top 5% o hacemos seleccion por ruleta
        for _ in range(int(DINOS_PER_GENERATION * 0.4)):
            father = self.select_parent_tournament(5)
            son = Dino()
            son.genome = father.genome.mutate()
            son.init_brain()
            new_dinos.append(son)
        
        # 20% crossover del top 5%
        for _ in range(int(DINOS_PER_GENERATION * 0.2)):
            father = self.select_parent_tournament(5)
            mother = self.select_parent_tournament(5)
            son = Dino()
            son.genome = father.genome.crossover(mother.genome)
            son.init_brain()
            new_dinos.append(son)
        
        self.dinos = new_dinos
    
    def next_obstacle_info(self, dino):
        """
        Encuentra el siguiente obstáculo para un dinosaurio.
        
        Args:
            dino: el dinosaurio
            
        Returns:
            list: [distancia, x, y, ancho, alto]
        """
        result = [1280, 0, 0, 0, 0]
        
        for enemy in self.enemies:
            if enemy.x_pos > dino.x_pos:
                result[0] = enemy.x_pos - dino.x_pos
                result[1] = enemy.x_pos
                result[2] = enemy.y_pos
                result[3] = enemy.obj_width
                result[4] = enemy.obj_height
                break
        
        return result
    
    def draw(self, screen, sprites, font, small_font):
        """
        Dibuja toda la simulación.
        
        Args:
            screen: superficie de pygame
            sprites: diccionario de sprites
            font: fuente grande
            small_font: fuente pequeña
        """
        # Dibujar suelo
        self.ground.draw(screen, sprites)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(screen, sprites)
        
        # Dibujar dinosaurios vivos
        for dino in self.dinos:
            if dino.alive:
                dino.draw(screen, sprites)
        
        # Dibujar información
        self.draw_info(screen, font, small_font)
    
    def draw_info(self, screen, font, small_font):
        """
        Dibuja la información de la simulación y la red neuronal.
        
        Args:
            screen: superficie de pygame
            font: fuente grande
            small_font: fuente pequeña
        """
        # Score
        score_text = font.render(str(self.score), True, (0, 0, 0))
        screen.blit(score_text, (1200, 80))
        
        # Información de generación
        gen_text = font.render(f"Generation: {self.generation}", True, (0, 0, 0))
        screen.blit(gen_text, (80, 80))
        
        avg_text = font.render(f"Average Score (last gen): {self.last_gen_avg_score}", True, (0, 0, 0))
        screen.blit(avg_text, (80, 120))
        
        max_text = font.render(f"Max Score (last gen): {self.last_gen_max_score}", True, (0, 0, 0))
        screen.blit(max_text, (80, 160))
        
        alive_text = font.render(f"Alive: {self.dinos_alive}", True, (0, 0, 0))
        screen.blit(alive_text, (80, 200))
        
        # Dibujar red neuronal del primer dino vivo
        self.draw_network(screen, small_font)
    
    def draw_network(self, screen, font):
        """
        Dibuja la visualización de la red neuronal del primer dino vivo.
        
        Args:
            screen: superficie de pygame
            font: fuente para texto
        """
        for dino in self.dinos:
            if dino.alive:
                dino.brain.draw(screen, font)
                self.best_weights=dino.brain.get_weights()
                break
    
    def tenth_of_second(self):
        """Ejecuta acciones cada décima de segundo."""
        # Alternar sprites de dinosaurios
        for dino in self.dinos:
            if dino.alive:
                dino.toggle_sprite()
        
        # Incrementar score
        self.score += 1
    
    def quarter_of_second(self):
        """Ejecuta acciones cada cuarto de segundo."""
        # Alternar sprites de enemigos
        for enemy in self.enemies:
            enemy.toggle_sprite()
    
    def spawn_enemy(self):
        """Genera un enemigo aleatorio (cactus o pájaro)."""
        if random.random() < 0.5:
            self.enemies.append(Cactus())
        else:
            self.enemies.append(Bird())

    def select_parent_tournament(self, k=5):
        """Selecciona un padre por torneo (elige k individuos al azar y toma el mejor)."""
        competitors = random.sample(self.dinos, k)
        return max(competitors, key=lambda d: d.score)
