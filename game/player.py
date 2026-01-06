import pygame
from game.level import Level
from item import Item

class Player:
    def __init__(self):
        self.pos : pygame.Vector2 = pygame.Vector2(0, 0)
        self.hp = 100
        self.maxhp = 100
        self.dmgmean = 15
        self.dmgdevt = 4
        self.gold = 50
        self.inventory : dict[Item, int] = {}

    def spawn(self, pos: tuple[int, int]):
        self.pos = pygame.Vector2(pos)

    def move(self, direction: pygame.Vector2 | tuple[int, int], level: Level):
        new_pos : pygame.Vector2 = self.pos + direction
        if level.is_walkable(new_pos):
            self.pos = new_pos
            
    def inventorySummary(self) -> str:
        return ""
