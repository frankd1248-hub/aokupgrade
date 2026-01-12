from __future__ import annotations
import pygame
from engine.scene import Scene
from game.uiButton import UIButton
from typing import Callable

class MenuScene (Scene):
    """_summary_
        A Menu for AOK. This is recommended to be initialized in a JSON-like format.
    """

    def __init__(
        self,
        prev_scene : Scene,
        bgcolor : tuple[int, int, int] = (255, 255, 255),
        buttons : list[UIButton] | None = None,
        texts : list[tuple[pygame.Surface, pygame.Rect]] | None = None,
        updatecb: Callable[[float], None] = lambda x: None,
        exit_on_esc : bool = True
    ):
        self.prev_scene = prev_scene
        self.bgcolor = bgcolor

        self.buttons = buttons or []
        self.texts = texts or []

        self.focused_index = 0 if self.buttons else -1
        self._update_focus()

        # Prevent key repeat spam
        self.nav_cooldown = 0
        self.nav_delay = 150  # ms
        
        self.updatecb = updatecb
        
        self._exit_on_esc = exit_on_esc

    def _update_focus(self):
        for i, btn in enumerate(self.buttons):
            btn.focused = (i == self.focused_index)
            
    def set_texts(self, texts: list[tuple[pygame.Surface, pygame.Rect]]) -> None:
        self.texts = texts

    def handle_event(self, event : pygame.event.Event):
        # Mouse support stays
        for button in self.buttons:
            if button.handle_event(event):
                return

        # Keyboard navigation
        if event.type == pygame.KEYDOWN:
            now = pygame.time.get_ticks()
            if now - self.nav_cooldown < self.nav_delay:
                return
            self.nav_cooldown = now

            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.focused_index = (self.focused_index + 1) % len(self.buttons)
                self._update_focus()

            elif event.key in (pygame.K_UP, pygame.K_w):
                self.focused_index = (self.focused_index - 1) % len(self.buttons)
                self._update_focus()

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.focused_index >= 0:
                    self.buttons[self.focused_index].activate()

            elif event.key == pygame.K_ESCAPE and self._exit_on_esc:
                self.gameobj.pop_scene()

    def update(self, dt: int):
        self.updatecb(dt)

    def render(self, surface: pygame.Surface):
        surface.fill(self.bgcolor)

        for button in self.buttons:
            button.draw(surface)

        for text_surface, rect in self.texts:
            surface.blit(text_surface, rect)
