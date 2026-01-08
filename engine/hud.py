import pygame
from abc import ABC, abstractmethod
from typing import Any

class HUD (ABC):
    """
    ABC for any HUD in any game, 2D or 3D.
    """
    
    def setGameobj(self, gameobj: Any):
        """
        This function sets self.gameobj to the given argument. This is used when adding a HUD to a Game.

        Args:
            gameobj (Any): The specific Game object to be bound to the HUD
        """
        self.gameobj = gameobj
    
    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        This is an abstract method that should be implemented by any child classes
        This should render the HUD to the given surface, without filling the surface ideally.

        Args:
            surface (pygame.Surface): The surface that should be drawn to
        """
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        This is an abstract method that should be implemented by any child classes.
        For example, you could update the HUD e.g. when a key is pressed.

        Args:
            event (pygame.event.Event): The event that should be processed
        """
        pass