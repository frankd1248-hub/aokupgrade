import pygame
from typing import Any

class Game:
    def __init__(self, scene : Any, frm : int = 60):
        pygame.init()
        pygame.display.set_caption("Advenchers of Kowawa")

        self.surface = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        self.scene = scene
        self.scene.setGameobj(self)
        self.running = True
        self.framerate = frm
        
    def setEscapeMenu(self, escapeMenu : Any):
        self.escapeMenu = escapeMenu
        
    def change_scene(self, scene : Any):
        self.scene = scene
        self.scene.setGameobj(self)
        
    def get_scene(self):
        return self.scene

    def run(self):
        while self.running:
            dt = self.clock.tick(self.framerate)
            self.handle_events()
            self.scene.update(dt)
            self.scene.render(self.surface)
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            self.scene.handle_event(event)
