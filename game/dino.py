import random
from game.game_object import GameObject
from neural_network.genome import Genome
from neural_network.brain import Brain


class Dino(GameObject):
    """
    Dinosaurio con red neuronal y genoma.
    Puede saltar, agacharse y morir al colisionar con enemigos.
    """
    
    def __init__(self):
        super().__init__()
        self.x_pos = random.randint(100, 300)
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86
        
        self.jump_stage = 0
        self.alive = True
        self.score = 0
        
        # Red neuronal
        self.genome = Genome()
        self.brain = None
        self.init_brain()
        self.brain_inputs = [0] * 7
        
        # Sprite
        self.sprite = "walking_dino_1"
        self.sprite_offset = [-4, -2]
    
    def init_brain(self):
        """Inicializa el cerebro (red neuronal) desde el genoma."""
        self.brain = Brain(self.genome)
    
    def update(self, next_obstacle_info, speed):
        """
        Actualiza el dinosaurio: lee sensores, decide acción, ejecuta física.
        
        Args:
            next_obstacle_info: información del siguiente obstáculo [distancia, x, y, ancho, alto]
            speed: velocidad actual del juego
        """
        if not self.alive:
            return
        
        self.update_brain_inputs(next_obstacle_info, speed)
        self.brain.feed_forward(self.brain_inputs)
        self.process_brain_output()
        
        if self.jumping():
            self.update_jump()
    
    def update_brain_inputs(self, next_obstacle_info, speed):
        """
        Normaliza y actualiza las entradas de la red neuronal.
        
        Args:
            next_obstacle_info: [distancia, x, y, ancho, alto] del obstáculo
            speed: velocidad del juego
        """
        self.brain_inputs[0] = next_obstacle_info[0] / 900  # distancia normalizada
        self.brain_inputs[1] = (next_obstacle_info[1] - 450) / (1350 - 450)  # x normalizada
        self.brain_inputs[2] = (next_obstacle_info[2] - 370) / (480 - 370)   # y normalizada
        self.brain_inputs[3] = (next_obstacle_info[3] - 30) / (146 - 30)     # ancho normalizado
        self.brain_inputs[4] = (next_obstacle_info[4] - 40) / (96 - 40)      # alto normalizado
        self.brain_inputs[5] = (self.y_pos - 278) / (484 - 278)              # y del dino normalizada
        self.brain_inputs[6] = (speed - 15) / (30 - 15)                      # velocidad normalizada
    
    def update_jump(self):
        """Actualiza la física del salto (parábola)."""
        self.y_pos = int(450 - ((-4 * self.jump_stage * (self.jump_stage - 1)) * 172))
        self.jump_stage += 0.03
        
        if self.jump_stage > 1:
            self.stop_jump()
    
    def process_brain_output(self):
        """
        Procesa las salidas de la red neuronal para ejecutar acciones.
        outputs[0] = saltar
        outputs[1] = agacharse
        """
        # Saltar
        if self.brain.outputs[0] != 0:
            if not self.crouching() and not self.jumping():
                self.jump()
        
        # Agacharse
        if self.brain.outputs[1] == 0:
            if self.crouching():
                self.stop_crouch()
        else:
            if self.jumping():
                self.stop_jump()
            self.crouch()
    
    def jump(self):
        """Inicia el salto."""
        self.jump_stage = 0.0001
        self.sprite = "standing_dino"
    
    def stop_jump(self):
        """Detiene el salto y vuelve al suelo."""
        self.jump_stage = 0
        self.y_pos = 450
        self.sprite = "walking_dino_1"
    
    def crouch(self):
        """Agacha al dinosaurio."""
        if not self.crouching():
            self.y_pos = 484
            self.obj_width = 110
            self.obj_height = 52
            self.sprite = "crouching_dino_1"
    
    def stop_crouch(self):
        """Deja de agacharse."""
        self.y_pos = 450
        self.obj_width = 80
        self.obj_height = 86
        self.sprite = "walking_dino_1"
    
    def jumping(self):
        """Verifica si está saltando."""
        return self.jump_stage > 0
    
    def crouching(self):
        """Verifica si está agachado."""
        return self.obj_width == 110
    
    def die(self, sim_score):
        """
        Mata al dinosaurio y guarda su score.
        
        Args:
            sim_score: score de la simulación cuando murió
        """
        self.alive = False
        self.score = sim_score
    
    def reset(self):
        """Resetea el dinosaurio para la siguiente generación."""
        self.alive = True
        self.score = 0
    
    def toggle_sprite(self):
        """Alterna entre sprites de animación."""
        if self.sprite == "walking_dino_1":
            self.sprite = "walking_dino_2"
        elif self.sprite == "walking_dino_2":
            self.sprite = "walking_dino_1"
        elif self.sprite == "crouching_dino_1":
            self.sprite = "crouching_dino_2"
        elif self.sprite == "crouching_dino_2":
            self.sprite = "crouching_dino_1"
    
    def __lt__(self, other):
        """Comparación para ordenamiento por score."""
        return self.score < other.score