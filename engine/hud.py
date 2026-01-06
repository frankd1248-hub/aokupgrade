import pygame
from abc import ABC, abstractmethod
from typing import Any

class HUD (ABC):
    
    def setGameobj(self, gameobj: Any):
        self.gameobj = gameobj
    
    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass