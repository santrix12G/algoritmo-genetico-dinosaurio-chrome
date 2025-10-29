import pygame


class GameObject:
    """Clase base abstracta para objetos del juego."""
    
    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.obj_width = 0
        self.obj_height = 0
        self.sprite = None
        self.sprite_offset = [0, 0]
    
    def draw(self, screen, sprites):
        """
        Dibuja el objeto en la pantalla.
        
        Args:
            screen: superficie de pygame
            sprites: diccionario de sprites
        """
        if self.sprite and self.sprite in sprites:
            screen.blit(sprites[self.sprite], 
                       (self.x_pos + self.sprite_offset[0], 
                        self.y_pos + self.sprite_offset[1]))
    
    def is_collisioning_with(self, another_object):
        """
        Verifica colisión con otro objeto usando AABB.
        
        Args:
            another_object: otro GameObject
            
        Returns:
            bool: True si hay colisión
        """
        return (self.x_pos + self.obj_width > another_object.x_pos and 
                self.x_pos < another_object.x_pos + another_object.obj_width and
                self.y_pos + self.obj_height > another_object.y_pos and 
                self.y_pos < another_object.y_pos + another_object.obj_height)
    
    def toggle_sprite(self):
        """Cambia entre sprites (para animaciones)."""
        pass


class Ground(GameObject):
    """Representa el suelo del juego."""
    
    def __init__(self):
        super().__init__()
        self.x_pos = 2400
        self.y_pos = 515
        self.sprite = "ground"
    
    def update(self, speed):
        """
        Actualiza la posición del suelo para crear efecto de movimiento.
        
        Args:
            speed: velocidad de desplazamiento
        """
        self.x_pos -= speed
        if self.x_pos <= 0:
            self.x_pos = 2400
    
    def draw(self, screen, sprites):
        """
        Dibuja el suelo con efecto de loop infinito.
        
        Args:
            screen: superficie de pygame
            sprites: diccionario de sprites
        """
        if self.sprite in sprites:
            screen.blit(sprites[self.sprite], (self.x_pos, self.y_pos))
            screen.blit(sprites[self.sprite], (self.x_pos - 2400, self.y_pos))