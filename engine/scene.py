import pygame
from abc import ABC, abstractmethod
from engine.game import Game

class Scene (ABC):
    
    @abstractmethod
    def setGameobj(self, gameobj: Game):
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass
    
    @abstractmethod
    def update(self, dt: int):
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass