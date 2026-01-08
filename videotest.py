#!./.venv/bin/python3.11

from engine.game import Game
from game.cutscene import Cutscene

scene = Cutscene("/home/frankdai/Documents/obs/aokdev1.mp4", 60)

game = Game(scene, 60)
game.run()