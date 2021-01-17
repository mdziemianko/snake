from world.world import *
from player.player import Player
from renderer.pygame import Renderer
from typing import Optional

class Game:
    def __init__(self, world: World, player: Player, renderer: Optional[Renderer] = None):
        self._world = world
        self._player = player
        self._renderer = renderer

    def play(self):
        running = True

        if self._renderer:
            self._renderer.prerender(self._world, self._player)
        while running:
            running = self._world.evolve()

            if self._renderer:
                self._renderer.render(self._world, self._player)

            move = self._player.get_direction(self._world)
            if move is not None:
                self._world.get_snake().set_direction(move)

        return self._world.get_score()

