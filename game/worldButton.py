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
        """
        Initializes a button in-world that can have an action

        Args:
            rect (pygame.Rect): A rectangle representing the position and size of the button (world coordinates)
            text (str): The text displayed on the button
            callback (Callable[[], None]): The action that should be performed when the button is clicked
            font (pygame.font.Font): Font that the text should be displayed in
            bg_color (tuple[int, int, int], optional): Background color of the text. Defaults to (60, 60, 60).
            border_color (tuple[int, int, int], optional): Color of the border. Defaults to (200, 200, 200).
            text_color (tuple[int, int, int], optional): Foreground color of the text. Defaults to (255, 255, 255).
        """
        
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

    def get_screen_rect(self, camera: Camera) -> pygame.Rect:
        """
        Returns the rectangle the button should be at (screen coordinates) given a Camera object.

        Args:
            camera (Camera): A camera object. Functionally a wrapper for a viewport.

        Returns:
            pygame.Rect: A rectangle, (width and height useless), just a wrapper for coordinate.
        """
        viewport = camera.get_viewport_rect()
        return pygame.Rect(
            self.rect.x - viewport.x,
            self.rect.y - viewport.y,
            self.rect.width,
            self.rect.height
        )

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        """
        Draws the button to the provided surface, with the position given by the transformation in the Camera.

        Args:
            surface (pygame.Surface): The surface to been drawn to
            camera (Camera): The camera. Used to get a linear transformation for the button position.
        """
        screen_rect = self.get_screen_rect(camera)

        # Draw button body
        pygame.draw.rect(surface, self.bg_color, screen_rect)
        pygame.draw.rect(surface, self.border_color, screen_rect, 2)

        # Draw text centered
        text_rect = self.text_surface.get_rect(center=screen_rect.center)
        surface.blit(self.text_surface, text_rect)

    def handle_click(self, mouse_pos: tuple[int, int] | pygame.Vector2, camera : Camera) -> bool:
        """
        Detects if the button was clicked on

        Args:
            mouse_pos (tuple[int, int] | pygame.Vector2): The position of the mouse, from the main event loop
            camera (Camera): Camera object

        Returns:
            bool: If the button was clicked on (True = yes)
        """
        if self.get_screen_rect(camera).collidepoint(mouse_pos):
            self.callback()
            return True
        return False
