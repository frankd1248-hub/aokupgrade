import pygame
from abc import ABC, abstractmethod
from typing import Any

class Scene (ABC):
    """
    ABC for any scene in the Game.
    """

    def setGameobj(self, gameobj: Any) -> None:
        """
        This function sets self.gameobj to the given argument. This is used when adding a Scene to a Game.

        Args:
            gameobj (Any): The specific Game object to be bound to the Scene
        """
        self.gameobj = gameobj
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """
        This is an abstract method that should be implemented by any child classes.
        The implementing Scene should ideally process any event passed in
        For example, you could update the Scene e.g. when a key is pressed with this method.

        Args:
            event (pygame.event.Event): The event that should be processed
        """
        pass
    
    @abstractmethod
    def update(self, dt: int):
        """
        This is an abstract method that should be implemented by any child classes.
        The implementing Scene will receive the amount of time that has passed in milliseconds.

        Args:
            dt (int): Amount of time that has passed since last frame, in milliseconds.
        """
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface):
        """
        This is an abstract method that should be implemented by any child classes.
        The implementing Scene will receive the surface that the scene should be drawn to.
        As the scene forms the bottom layer of the graphics, it is okay for it to use fill on the surface.

        Args:
            surface (pygame.Surface): The surface that should be drawn to.
        """
        pass