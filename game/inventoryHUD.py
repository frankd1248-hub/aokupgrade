from engine.hud import HUD
from typing import Callable
from pygame.event import Event
import pygame

class InventoryHUD (HUD):
    
    def __init__(self, texts: Callable[[], str], font: pygame.font.Font):
        self.texts = texts
        self.font = font
        
    def handle_event(self, event: Event):
        pass
    
    def render(self, surface: pygame.Surface):
        textSurf = self.rendermulti(self.texts())
        surface.blit(textSurf.subsurface((0, 0), (400, 200)), (624, 0))
        
    def rendermulti(self, text : str) -> pygame.Surface:
        resultSurface = pygame.Surface((400, 40 * (text.count("\n")+1)))
        for i, line in enumerate(text.splitlines()):
            surf = self.font.render(line, True, (0, 0, 0))
            resultSurface.blit(surf, (0, i*40))
        return resultSurface