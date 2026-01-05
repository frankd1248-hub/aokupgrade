import pygame
from game.worldButton import WorldButton

class Level:
    """
        An AOK level. This can be initialized in a JSON-like format for ease.
    """
    
    def __init__(self, map_path : str, spawn_pos : tuple[int, int], buttons : list[WorldButton] | None = None):
        self.map = pygame.image.load(map_path)
        self.map = pygame.transform.scale(self.map, (9000, 9000))

        self.spawn_pos = pygame.Vector2(spawn_pos)
        self.path_color = self.map.get_at(spawn_pos)

        self.buttons = buttons or []

    def is_walkable(self, pos : pygame.Vector2):
        x, y = int(pos.x), int(pos.y)
        if not (0 <= x < self.map.get_width() and 0 <= y < self.map.get_height()):
            return False
        return self.map.get_at((x, y)) == self.path_color
