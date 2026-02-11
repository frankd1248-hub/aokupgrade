from game.menuScene import MenuScene
from engine.game import Game
from game.uiButton import UIButton
from game.player import Player
from game.gameplayScene import GameplayScene
from item import Item, getItem
from pygame.font import Font
from pygame import Rect
from pygame import Vector2 as Pair
from pygame import Surface
from typing import Callable, Any
from random import gauss as getrandom, uniform as random

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

    # --- enemy stats ---
    enemyhp, enemydmgmean, enemydmgdevt, enemymercyodds = getEnemyStats(name)

    state : dict[str, Any] = {
        "enemyhp": enemyhp,
        "player_turn": True,
        "message": f"{name} stands in your way."
    }

    # --- end scenes ---
    winScene = MenuScene(
        game.peek_scene(),
        bgcolor = (30, 30, 30),
        texts=[(
            font.render("YOU WIN! (Enemy defeated)", True, (255, 255, 255)),
            Rect(300, 300, 500, 50)
        )]
    )

    loseScene = MenuScene(
        game.peek_scene(),
        bgcolor = (30, 30, 30),
        texts=[(
            font.render("YOU LOST...", True, (255, 255, 255)),
            Rect(300, 300, 500, 50)
        )]
    )

    # --- helpers ---
    def refresh_text(scene: MenuScene):
        scene.set_texts([
            (
                font.render(
                    f"{name} HP: {max(0, state['enemyhp'])}    "
                    f"Your HP: {player.hp}/{player.maxhp}",
                    True, (255, 255, 255)
                ),
                Rect(40, 40, 800, 40)
            ),
            (
                font.render(state["message"], True, (255, 255, 255)),
                Rect(40, 100, 900, 40)
            )
        ])

    # --- player actions ---
    def player_attack():
        if not state["player_turn"]:
            return

        dmg = round(getrandom(player.dmgmean, player.dmgdevt))
        state["enemyhp"] -= dmg
        state["message"] = f"You attack {name} for {dmg} damage!"
        state["player_turn"] = False

        if state["enemyhp"] <= 0:
            game.pop_scene()
            game.push_scene(winScene)
            player.move(
                Pair(
                    tpLocation[0] - player.pos[0],
                    tpLocation[1] - player.pos[1]
                ),
                game.peek_next_scene().levels[tpLocation[2]] # type: ignore
            )
            return

    def open_items():
        if not state["player_turn"]:
            return

        buttons : list[UIButton] = []
        y = 200

        for item, count in player.inventory.items():
            if count <= 0:
                continue

            def make_cb(it : Item = item):
                def use():
                    if not state["player_turn"]:
                        return
                    it.use(player)
                    player.inventory[it] -= 1
                    state["message"] = f"You used {it.name}."
                    state["player_turn"] = False
                    game.pop_scene()
                return use

            buttons.append(
                UIButton(
                    Rect(300, y, 400, 40),
                    f"{item.name} x{count}",
                    make_cb(),
                    font
                )
            )
            y += 50

        itemScene = MenuScene(
            game.peek_scene(),
            bgcolor=(40, 20, 20),
            buttons=buttons,
            texts=[(
                font.render("Choose an item:", True, (255, 255, 255)),
                Rect(300, 150, 400, 40)
            )]
        )

        game.push_scene(itemScene)

    def try_mercy():
        if not state["player_turn"]:
            return

        if tame and tame(player):
            state["message"] = f"{name} was tamed!"
            game.pop_scene()
            game.push_scene(winScene)
            player.move(
                Pair(
                    tpLocation[0] - player.pos[0],
                    tpLocation[1] - player.pos[1]
                ),
                game.peek_next_scene().levels[tpLocation[2]]  # type: ignore
            )
        elif round(random(0, enemymercyodds)) == 1:
            state["message"] = f"{name} was spared!"
            game.pop_scene()
            game.push_scene(winScene)
            player.move(
                Pair(
                    tpLocation[0] - player.pos[0],
                    tpLocation[1] - player.pos[1]
                ),
                game.peek_next_scene().levels[tpLocation[2]]  # type: ignore
            )
        else:
            state["message"] = f"{name} refuses your mercy."
            state["player_turn"] = False

    # --- enemy turn ---
    def enemy_turn(float: int):
        if state["player_turn"]:
            return

        dmg = round(getrandom(enemydmgmean, enemydmgdevt))
        dmg = max(0, dmg)
        player.hp -= dmg

        if player.hp <= 0:
            game.pop_scene()
            game.push_scene(loseScene)
            return

        state["message"] = f"{name} hits you for {dmg} damage!"
        state["player_turn"] = True
        
    def update(dt: float):
        enemy_turn(int(dt))
        refresh_text(scene)

    # --- main fight scene ---
    scene = MenuScene(
        game.peek_scene(),
        bgcolor=(60, 30, 20),
        buttons=[
            UIButton(
                Rect(106, 620, 200, 50),
                "FIGHT",
                player_attack,
                font,
                (10, 10, 10), (200, 30, 0),
                (240, 70, 0), (204, 0, 0)
            ),
            UIButton(
                Rect(412, 620, 200, 50),
                "ITEM",
                open_items,
                font,
                (10, 10, 10), (200, 30, 0),
                (240, 70, 0), (204, 0, 0)
            ),
            UIButton(
                Rect(718, 620, 200, 50),
                "MERCY",
                try_mercy,
                font,
                (10, 10, 10), (200, 30, 0),
                (240, 70, 0), (204, 0, 0)
            )
        ],
        texts=[],
        exit_on_esc=False
    )
    
    scene.updatecb = update

    refresh_text(scene)
    game.push_scene(scene)
    
    

def canTameIdiotlax(player: Player) -> bool:
    return "dusty_bun" in player.inventory.keys()

def getEnemyStats(name: str) -> tuple[int, int, int, int]:
    if name == "Idiotlax":            return (100, 5, 4, 10)
    return (0, 0, 0, 1)