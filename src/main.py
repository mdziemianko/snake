import random
import numpy as np

random.seed(34)
np.random.seed(42)

import pygame as pg
from world import World
from renderer import Renderer
from geometry import *
from player import HumanPlayer, Player, NNPlayer
from world.game import Game


def run(player: Player):
    renderer = Renderer(player.get_speed())

    should_quit = False
    while not should_quit:
        world = World()

        game = Game(world, player, renderer)

        score = game.play()

        renderer.display_game_over(score)
        should_quit = wait_for_decision()



def wait_for_decision() -> bool:
    while True:
        event = pg.event.wait()
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            return True
        elif event.type == pg.KEYDOWN:
            return False



if __name__ == "__main__":
    import sys

    player = HumanPlayer(10, "human") if len(sys.argv) == 1 else NNPlayer.from_file(sys.argv[1])

    run(player)