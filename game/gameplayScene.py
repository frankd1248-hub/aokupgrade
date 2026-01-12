import pygame
from engine.camera import Camera
from engine.scene import Scene
from game.player import Player
from game.level import Level
from game.menuScene import MenuScene
from game.uiButton import UIButton

MOVE_SPEED = 7

class GameplayScene (Scene):
    """_summary_
        A gameplay scene, initialized by a list of levels. This can be initialized in a JSON-like format for ease.
    """
    
    def __init__(self, levels: list[Level], buttons: list[UIButton] = []):
        self.player = Player()
        self.camera = Camera(1024, 768)

        self.levels = levels
        self.current_level_index = 0
        self.buttons = buttons
        self.load_level(0)
        
    def setPlayer(self, player: Player):
        self.player = player
        self.camera = Camera(1024, 768)
        self.current_level_index = 0
        self.load_level(0)
        self.playersprite = pygame.image.load("./assets/player.png").convert_alpha()
        self.playersprite = pygame.transform.smoothscale(self.playersprite, (160, 240))
    
    def setPausemenu(self, menu: MenuScene):
        self.pause_menu = menu

    def load_level(self, index: int):
        self.current_level = self.levels[index]
        self.player.spawn((int(self.current_level.spawn_pos.x), int(self.current_level.spawn_pos.y)))

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.current_level.buttons:
                if button.handle_click(event.pos, self.camera):
                    break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.gameobj.push_scene(self.pause_menu)
                
    def remove_wbutton(self, level: int, idx: int) -> None:
        self.levels[level].buttons.pop(idx)

    def update(self, dt: int):
        keys = pygame.key.get_pressed()

        move_amount = MOVE_SPEED * dt / 16.6666667
        if keys[pygame.K_w] and self.player.pos.y >= 386:
            self.player.move(pygame.Vector2(0, -move_amount), self.current_level)
        if keys[pygame.K_a] and self.player.pos.x >= 514:
            self.player.move(pygame.Vector2(-move_amount, 0), self.current_level)
        if keys[pygame.K_s] and self.player.pos.y <= 8614:
            self.player.move(pygame.Vector2(0, move_amount), self.current_level)
        if keys[pygame.K_d] and self.player.pos.x <= 8486:
            self.player.move(pygame.Vector2(move_amount, 0), self.current_level)

        self.camera.update(self.player.pos)

    def render(self, surface: pygame.Surface):
        viewport = self.camera.get_viewport_rect()
        surface.blit(self.current_level.map.subsurface(viewport), (0, 0))

        for button in self.current_level.buttons:
            button.draw(surface, self.camera)
            
        for button in self.buttons:
            button.draw(surface)

        surface.blit(self.playersprite, pygame.Rect(
            432, 264, 80, 120
        ))