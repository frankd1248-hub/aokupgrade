import pygame

class Camera:
    def __init__(self, width : int, height : int):
        self.width = width
        self.height = height
        self.viewport = pygame.Rect(0, 0, width, height)

    def update(self, target_pos : pygame.Vector2):
        self.viewport.x = int(target_pos.x - self.width // 2)
        self.viewport.y = int(target_pos.y - self.height // 2)

    def get_viewport_rect(self):
        return self.viewport
