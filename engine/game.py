import pygame
from collections import deque as stack
from engine.scene import Scene
from engine.hud import HUD

class Game:
    def __init__(self, scene : Scene, frm : int = 60):
        pygame.init()
        pygame.display.set_caption("Advenchers of Kowawa")

        self.surface = pygame.display.set_mode((1024, 768))
        self.clock = pygame.time.Clock()
        self.running = True
        self.framerate = frm
        
        self.scenestack = stack([scene])
        self.scenestack[-1].setGameobj(self)
        
        self.HUDlist : list[HUD] = []
        
    def setEscapeMenu(self, escapeMenu : Scene):
        self.escapeMenu = escapeMenu
        
    def add_hud(self, hud: HUD):
        self.HUDlist.append(hud)
        
    def peek_scene(self):
        return self.scenestack[-1]

    def pop_scene(self):
        self.scenestack.pop()
        
    def push_scene(self, scene: Scene):
        self.scenestack.append(scene)
        self.scenestack[-1].setGameobj(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.framerate)
            self.handle_events()
            self.scenestack[-1].update(dt)
            self.scenestack[-1].render(self.surface)
            for hud in self.HUDlist:
                hud.render(self.surface)
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            self.scenestack[-1].handle_event(event)
