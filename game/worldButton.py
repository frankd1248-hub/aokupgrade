import pygame
from engine.camera import Camera
from typing import Callable

class WorldButton:
    
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Callable[[], None],
        font: pygame.font.Font,
        bg_color : tuple[int, int, int] = (60, 60, 60),
        border_color : tuple[int, int, int] = (200, 200, 200),
        text_color : tuple[int, int, int] = (255, 255, 255)
    ):
        # rect is in WORLD coordinates
        self.rect = rect
        self.text = text
        self.callback = callback

        self.font = font
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color

        # Pre-render text surface
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def get_screen_rect(self, camera: Camera):
        viewport = camera.get_viewport_rect()
        return pygame.Rect(
            self.rect.x - viewport.x,
            self.rect.y - viewport.y,
            self.rect.width,
            self.rect.height
        )

    def draw(self, surface: pygame.Surface, camera: Camera):
        screen_rect = self.get_screen_rect(camera)

        # Draw button body
        pygame.draw.rect(surface, self.bg_color, screen_rect)
        pygame.draw.rect(surface, self.border_color, screen_rect, 2)

        # Draw text centered
        text_rect = self.text_surface.get_rect(center=screen_rect.center)
        surface.blit(self.text_surface, text_rect)

    def handle_click(self, mouse_pos: tuple[int, int] | pygame.Vector2, camera : Camera):
        if self.get_screen_rect(camera).collidepoint(mouse_pos):
            self.callback()
            return True
        return False
