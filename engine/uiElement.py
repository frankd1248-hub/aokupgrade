import pygame
from abc import ABC, abstractmethod
from typing import Any

class UIElement (ABC):
    """
    ABC for every UI element that could be implemented in any game.
    Contains two abstract methods:
    draw(self, surface: pygame.Surface) -> Any,
    handle_event(self, event: pygame.event.Event) -> Any.
    """
    
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> Any:
        """
        This is an abstract method that should be implemented by any child classes.
        When invoked, this method will draw the UI Element to the Surface provided.
        
        Args:
            surface (pygame.Surface): The surface that should be drawn to
        
        Returns:
            Any: Feel free to use the return value of this to signal any change in global state.
        """
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Any:
        """
        This is an abstract method that should be implemented by any child classes.
        When invoked, the UI Element will process an event.

        Args:
            event (pygame.event.Event): The event intended to be processed by the UI Element.

        Returns:
            Any: _description_
        """
        pass