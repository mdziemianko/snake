from player.player import Player
from world import World
from geometry import Direction
import pygame as pg

class HumanPlayer(Player):
    def __init__(self, speed: int, name: str):
        self._speed = speed
        self._name = name

    def get_direction(self, _: World):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    return Direction.UP
                elif event.key == pg.K_DOWN:
                    return Direction.DOWN
                elif event.key == pg.K_LEFT:
                    return Direction.LEFT
                elif event.key == pg.K_RIGHT:
                    return Direction.RIGHT
        return None

    def get_speed(self) -> int:
        return self._speed

    def get_name(self) -> str:
        return self._name