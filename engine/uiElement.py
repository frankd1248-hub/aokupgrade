import pygame
from abc import ABC, abstractmethod
from typing import Any

class UIElement (ABC):
    
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Any:
        pass