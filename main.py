#!./.venv/bin/python3.11

"""
This is a project I started in C many years ago.
In January 2026, I decided I would re-start it at a completely new level, so here I am.
"""

from engine.game import Game
from game.gameplayScene import GameplayScene
from game.level import Level
from game.worldButton import WorldButton
from game.menuScene import MenuScene
from game.uiButton import UIButton
from game.player import Player
from game.inventoryHUD import InventoryHUD
import buttoncbs
import pygame

pygame.font.init()
font = pygame.font.Font("assets/font.ttf", 24) 
defaultKeybinds : dict[str, int] = {
    "mv_up": pygame.K_w,
    "mv_left": pygame.K_a,
    "mv_right": pygame.K_d,
    "mv_down": pygame.K_s
}

userKeybinds = defaultKeybinds

game : Game
gameScene : GameplayScene
player : Player = Player()

level1Buttons = [
    WorldButton (
        pygame.Rect(1542, 3948, 225, 50),
        "Enter the shop",
        lambda: buttoncbs.shop(game, font, player),
        font
    ), WorldButton (
        pygame.Rect(2940, 4680, 200, 50),
        "Pick it up?",
        lambda: buttoncbs.addItem(game, font, player, "dusty_bun", 0, 1),
        font
    ), WorldButton (
        pygame.Rect(3894, 5859, 150, 50),
        "FIGHT!",
        lambda: buttoncbs.fight(game, font, player, "Idiotlax", (4812, 5889, 0), tame = buttoncbs.canTameIdiotlax),
        font
    )
]

levels = [
    Level("assets/map1.png", (200 * 3, 1419 * 3), level1Buttons)
]

def resume():
    game.pop_scene()
    
def quit_game():
    pygame.quit()
    raise SystemExit

gameScene = GameplayScene(levels)
game = Game(gameScene, 60)

menu = MenuScene(
    prev_scene=gameScene,
    bgcolor=(30, 30, 30),
    buttons=[
        UIButton(
            pygame.Rect(412, 300, 200, 50),
            "Resume",
            resume,
            font
        ),
        UIButton(
            pygame.Rect(412, 380, 200, 50),
            "Quit",
            quit_game,
            font
        ),
    ],
    texts=[
        (
            font.render("Paused", True, (255, 255, 255)),
            pygame.Rect(464, 200, 312, 50)
        )
    ]
)

inventoryHUD = InventoryHUD (
    lambda: player.inventorySummary(),
    font
)

gameScene.setPausemenu(menu)
gameScene.setPlayer(player)

game.run()
