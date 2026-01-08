import pygame
from engine.uiElement import UIElement
from typing import Callable

class UIButton (UIElement):
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Callable[[], None],
        font: pygame.font.Font,
        bg_color: tuple[int, int, int] = (60, 60, 60),
        border_color: tuple[int, int, int] = (200, 200, 200),
        focus_color: tuple[int, int, int] = (255, 255, 0),
        text_color: tuple[int, int, int] = (255, 255, 255)
    ):
        """
        A button that can be placed in a MenuScene.

        Args:
            rect (pygame.Rect): Stores location and size of the button
            text (str): Text to be displayed on top of the button
            callback (Callable[[], None]): The action to be performed when the button is clicked
            font (pygame.font.Font): The font the text should be displayed in
            bg_color (tuple[int, int, int], optional): The background color of the text. Defaults to (60, 60, 60).
            border_color (tuple[int, int, int], optional): The color of the border of the button. Defaults to (200, 200, 200).
            focus_color (tuple[int, int, int], optional): The color of the border of the button when navigated to with the keyboard. Defaults to (255, 255, 0).
            text_color (tuple[int, int, int], optional): The foreground color of the text. Defaults to (255, 255, 255
        """
        self.rect = rect
        self.text = text
        self.callback = callback
        self.font = font

        self.bg_color = bg_color
        self.border_color = border_color
        self.focus_color = focus_color
        self.text_color = text_color

        self.focused = False
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def draw(self, surface: pygame.Surface):
        """
        Draws the button to a given surface.

        Args:
            surface (pygame.Surface): The surface to be drawn to
        """
        pygame.draw.rect(surface, self.bg_color, self.rect)

        border = self.focus_color if self.focused else self.border_color
        pygame.draw.rect(surface, border, self.rect, 3)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def activate(self):
        """
        Calls the callback when the button is clicked on by the cursor or enter is clicked while the button is focused on
        """
        self.callback()

    def handle_event(self, event: pygame.event.Event):
        """
        Handles mouse clicks
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.activate()
                return True
        return False
