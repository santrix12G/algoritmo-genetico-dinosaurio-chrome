"""
Clases de enemigos: Cactus y Bird (Pájaro).
"""
import random
from game.game_object import GameObject


class Enemy(GameObject):
    """Clase base para enemigos."""
    
    def __init__(self):
        super().__init__()
        self.x_pos = 1350
    
    def update(self, speed):
        """
        Mueve el enemigo hacia la izquierda.
        
        Args:
            speed: velocidad de movimiento
        """
        self.x_pos -= speed
    
    def is_offscreen(self):
        """
        Verifica si el enemigo salió de la pantalla.
        
        Returns:
            bool: True si está fuera de la pantalla
        """
        return self.x_pos + self.obj_width < 0


class Cactus(Enemy):
    """Cactus como obstáculo."""
    
    # Propiedades de cada tipo de cactus
    CACTUS_WIDTHS = [30, 64, 98, 46, 96, 146]
    CACTUS_HEIGHTS = [66, 66, 66, 96, 96, 96]
    CACTUS_Y_POS = [470, 470, 470, 444, 444, 444]
    
    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 5)
        self.obj_width = self.CACTUS_WIDTHS[self.type]
        self.obj_height = self.CACTUS_HEIGHTS[self.type]
        self.y_pos = self.CACTUS_Y_POS[self.type]
        self.sprite = f"cactus_type_{self.type + 1}"
        self.sprite_offset = [-2, -2]


class Bird(Enemy):
    """Pájaro volador como obstáculo."""
    
    # Alturas posibles para el pájaro
    BIRD_Y_POS = [435, 480, 370]
    
    def __init__(self):
        super().__init__()
        self.x_pos = 1350
        self.obj_width = 84
        self.obj_height = 40
        self.type = random.randint(0, 2)
        self.y_pos = self.BIRD_Y_POS[self.type]
        self.sprite = "bird_flying_1"
        self.sprite_offset = [-4, -16]
    
    def toggle_sprite(self):
        """Alterna entre los sprites de vuelo del pájaro."""
        if self.sprite == "bird_flying_1":
            self.sprite = "bird_flying_2"
        else:
            self.sprite = "bird_flying_1"