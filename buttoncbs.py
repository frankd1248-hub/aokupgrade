from game.menuScene import MenuScene
from engine.game import Game
from game.uiButton import UIButton
from game.player import Player
from pygame.font import Font
from pygame import Rect

def buyHeal(game: Game, font: Font, player: Player, amount: int, price: int):
    scene = MenuScene(
        game.get_scene(),
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
    
    game.change_scene(scene)
    
def buyDamage(game: Game, font: Font, player: Player, amount: int, price: int):
    scene = MenuScene(
        game.get_scene(),
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
    
    game.change_scene(scene)

def shop(game: Game, font : Font, player: Player):
    shopScene = MenuScene(
        game.get_scene(),
        bgcolor = (100, 150, 100),
        buttons = [
            UIButton(Rect(900, 150, 74, 40), "Buy", lambda: buyHeal(game, font, player, 15, 15), font),
            UIButton(Rect(900, 200, 75, 40), "Buy", lambda: buyHeal(game, font, player, 40, 35), font),
            UIButton(Rect(900, 250, 75, 40), "Buy", lambda: buyHeal(game, font, player, 95, 75), font)
        ],
        texts = [ 
            (
                font.render("SHOP", True, (0, 0, 0)),
                Rect(480, 50, 84, 40)
            ), (
                font.render(f"Current gold: {player.gold}, Current health: {player.hp}, Current attack damage: {player.dmgmean}", True, (0, 0, 0)), 
                Rect(50, 100, 825, 40)
            ), (
                font.render("Heal 15HP                         15G", True, (0, 0, 0)), 
                Rect(50, 150, 825, 40)
            ), (
                font.render("Heal 40HP                         35G", True, (0, 0, 0)), 
                Rect(50, 200, 825, 40)
            ), (
                font.render("Heal 95HP                         75G", True, (0, 0, 0)), 
                Rect(50, 250, 825, 40)
            ), (
                font.render("Increase attack damage by 15      25G", True, (0, 0, 0)),
                Rect(50, 300, 825, 40)
            ), (
                font.render("Increase attack damage by 35      55G", True, (0, 0, 0)),
                Rect(50, 350, 825, 40)
            ), (
                font.render("Increase attack damage by 75     100G", True, (0, 0, 0)),
                Rect(50, 400, 825, 40)
            )
        ]
    )
    game.change_scene(shopScene)
    
    return