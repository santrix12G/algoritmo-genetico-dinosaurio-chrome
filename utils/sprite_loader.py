"""
Carga y gestión de sprites desde el sprite sheet.
"""
import pygame


def initialize_sprites():
    """
    Carga todos los sprites desde el sprite sheet.
    
    Returns:
        dict: Diccionario con todos los sprites del juego
    """
    game_sprites = {}
    
    try:
        sprite_sheet = pygame.image.load("sprites.png").convert_alpha()
    except pygame.error as e:
        print(f"Error: No se pudo cargar 'sprites.png'. Asegúrate de que el archivo está en la raíz del proyecto.")
        print(f"Detalles: {e}")
        raise
    
    # Dinosaurio
    game_sprites["standing_dino"] = sprite_sheet.subsurface((1338, 2, 88, 94))
    game_sprites["walking_dino_1"] = sprite_sheet.subsurface((1514, 2, 88, 94))
    game_sprites["walking_dino_2"] = sprite_sheet.subsurface((1602, 2, 88, 94))
    game_sprites["dead_dino"] = sprite_sheet.subsurface((1690, 2, 88, 94))
    game_sprites["crouching_dino_1"] = sprite_sheet.subsurface((1866, 36, 118, 60))
    game_sprites["crouching_dino_2"] = sprite_sheet.subsurface((1984, 36, 118, 60))
    
    # Cactus
    game_sprites["cactus_type_1"] = sprite_sheet.subsurface((446, 2, 34, 70))
    game_sprites["cactus_type_2"] = sprite_sheet.subsurface((480, 2, 68, 70))
    game_sprites["cactus_type_3"] = sprite_sheet.subsurface((548, 2, 102, 70))
    game_sprites["cactus_type_4"] = sprite_sheet.subsurface((652, 2, 50, 100))
    game_sprites["cactus_type_5"] = sprite_sheet.subsurface((702, 2, 100, 100))
    game_sprites["cactus_type_6"] = sprite_sheet.subsurface((802, 2, 150, 100))
    
    # Pájaros
    game_sprites["bird_flying_1"] = sprite_sheet.subsurface((260, 2, 92, 80))
    game_sprites["bird_flying_2"] = sprite_sheet.subsurface((352, 2, 92, 80))
    
    # Suelo
    game_sprites["ground"] = sprite_sheet.subsurface((2, 104, 2400, 24))
    
    return game_sprites