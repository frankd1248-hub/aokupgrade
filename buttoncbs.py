from game.menuScene import MenuScene
from engine.game import Game
from game.uiButton import UIButton
from game.player import Player
from game.gameplayScene import GameplayScene
from item import getItem
from pygame.font import Font
from pygame import Rect
from pygame import Vector2 as Pair
from pygame import Surface
from typing import Callable

def buyHeal(game: Game, font: Font, player: Player, amount: int, price: int) -> None:
    scene = MenuScene(
        game.peek_scene(),
        bgcolor = (100, 150, 100),
        buttons = [],
        texts = [ (
                font.render (
                    f"You got healed {amount}HP!" if player.gold >= price and player.hp != player.maxhp 
                    else ("You didn't have enough money." if player.gold < price else "You are at full health."), 
                    True, (0, 0, 0)
                ),
                Rect(300, 300, 724, 50)
            )
        ]
    )
    
    player.hp += (amount if player.gold >= price and player.hp != player.maxhp else 0)
    player.hp = (player.maxhp if player.hp > player.maxhp else player.hp)
    player.gold -= (price if player.gold >= price and player.hp != player.maxhp else 0)
    
    game.push_scene(scene)
    
def buyDamage(game: Game, font: Font, player: Player, amount: int, price: int) -> None:
    scene = MenuScene(
        game.peek_scene(),
        bgcolor = (100, 150, 100),
        buttons = [],
        texts = [ (
                font.render (
                    f"You gained {amount} attack damage!" if player.gold >= price
                    else "You didn't have enough money.", 
                    True, (0, 0, 0)
                ),
                Rect(300, 300, 724, 50)
            )
        ]
    )
    
    player.dmgmean += (amount if player.gold >= price else 0)
    player.gold -= (price if player.gold >= price else 0)
    
    game.push_scene(scene)

def shop(game: Game, font : Font, player: Player) -> None:
    shoptext = [ 
        (
            font.render("SHOP", True, (0, 0, 0)),
            Rect(480, 50, 84, 40)
        ), (
            font.render(f"Current gold: {player.gold}, Current health: {player.hp}, Current attack damage: {player.dmgmean}", True, (0, 0, 0)), 
            Rect(50, 100, 825, 40)
        ), (
            font.render("Heal 15HP                         15G", True, (0, 0, 0)), 
            Rect(50, 200, 825, 40)
        ), (
            font.render("Heal 40HP                         35G", True, (0, 0, 0)), 
            Rect(50, 250, 825, 40)
        ), (
            font.render("Heal 95HP                         75G", True, (0, 0, 0)), 
            Rect(50, 300, 825, 40)
        ), (
            font.render("Increase attack damage by 15      25G", True, (0, 0, 0)),
            Rect(50, 350, 825, 40)
        ), (
            font.render("Increase attack damage by 35      55G", True, (0, 0, 0)),
            Rect(50, 400, 825, 40)
        ), (
            font.render("Increase attack damage by 75     100G", True, (0, 0, 0)),
            Rect(50, 450, 825, 40)
        )
    ]
    
    shopScene = MenuScene(
        game.peek_scene(),
        bgcolor = (100, 150, 100),
        buttons = [
            UIButton(Rect(900, 200, 74, 40), "Buy", lambda: buyHeal(game, font, player, 15, 15), font),
            UIButton(Rect(900, 250, 75, 40), "Buy", lambda: buyHeal(game, font, player, 40, 35), font),
            UIButton(Rect(900, 300, 75, 40), "Buy", lambda: buyHeal(game, font, player, 95, 75), font),
            UIButton(Rect(900, 350, 74, 40), "Buy", lambda: buyDamage(game, font, player, 15, 25), font),
            UIButton(Rect(900, 400, 75, 40), "Buy", lambda: buyDamage(game, font, player, 35, 55), font),
            UIButton(Rect(900, 450, 75, 40), "Buy", lambda: buyDamage(game, font, player, 75, 100), font)
        ],
        texts = shoptext,
        updatecb = lambda dt: changeShopText(shoptext, font, player, shopScene)
    )
    game.push_scene(shopScene)
    
    return

def changeShopText(original: list[tuple[Surface, Rect]], font: Font, player: Player, scene: MenuScene) -> None:
    original[1] = (
        font.render(f"Current gold: {player.gold}, Current health: {player.hp}, Current attack damage: {player.dmgmean}", True, (0, 0, 0)), 
        Rect(50, 100, 825, 40)
    )
    scene.set_texts(original)

def addItem(game: Game, font: Font, player: Player, itemID: str, level: int | None = None, buttonToRemove: int | None = None) -> None:
    item = getItem(itemID)
    
    if buttonToRemove is not None and isinstance(game.peek_scene(), GameplayScene):
        game.peek_scene().remove_wbutton(level, buttonToRemove) # type: ignore
    
    scene = MenuScene (
        game.peek_scene(),
        (150, 150, 150),
        buttons = [],
        texts = [
            (
                font.render(f"You gained a {item.name}!", True, (0, 0, 0)),
                Rect(300, 300, 724, 50)
            )
        ]
    )
    
    if item in player.inventory.keys():
        player.inventory[item] += 1
    else:
        player.inventory[item] = 1
    
    game.push_scene(scene)
    return 

def fight(game: Game, font: Font, player: Player, name: str, tpLocation: tuple[int, int, int], tame: Callable[[Player], bool] | None = None):
    player.move(Pair (
        tpLocation[0] - player.pos[0],
        tpLocation[1] - player.pos[1]
    ), game.peek_scene().levels[tpLocation[2]]) # type: ignore
    
    scene = MenuScene (
        game.peek_scene(),
        bgcolor = (60, 30, 20),
        buttons = [
            UIButton(
                Rect(106, 620, 200, 50),
                "FIGHT!",
                lambda: None,
                font,
                (10, 10, 10), (200, 30, 0),
                (240, 70, 0), (204, 0, 0)
            ), UIButton(
                Rect(412, 620, 200, 50),
                "ITEMS!",
                lambda: None,
                font,
                (10, 10, 10), (200, 30, 0),
                (240, 70, 0), (204, 0, 0)
            ), UIButton(
                Rect(718, 620, 200, 50),
                "MERCY!",
                lambda: None,
                font,
                (10, 10, 10), (200, 30, 0),
                (240, 70, 0), (204, 0, 0)
            )
        ],
        texts = [],
        exit_on_esc = False
    )
    
    game.push_scene(scene)

def canTameIdiotlax(player: Player) -> bool:
    return False