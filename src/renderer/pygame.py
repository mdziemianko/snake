import pygame as pg
from geometry import Point
from enum import Enum
from typing import List
from world.world import World
from player.player import Player

SQUARE_SIZE = 20
INFO_PANEL_SIZE = 300

class Color(Enum):
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

class Renderer:
    def __init__(self, speed):
        pg.init()
        self._grid_size = None
        self._screen = None
        pg.font.init()
        self._font = pg.font.SysFont('Comic Sans MS', 30)
        self._speed = speed
        self._clock = pg.time.Clock()

    def prerender(self, world: World, player: Player):
        self.render_grid(World.size)
        self.render_snake(world.get_snake().get_body())
        self.render_apple(world.get_apple_position())
        self.display_info(world, player)
        self.update()

    def render(self, world, player: Player):
        self._clock.tick(self._speed)
        self.render_apple(world.get_apple_position())
        vacated = world.get_snake().get_vacated()
        if vacated is not None:
            self.remove_snake_block(vacated)
        self.add_snake_block(world.get_snake().head(), is_head=True)
        self.add_snake_block(world.get_snake().get_body()[1])
        self.display_info(world, player)
        self.update()


    def render_grid(self, size: int):
        self._grid_size = size
        self._screen = pg.display.set_mode((size * SQUARE_SIZE + INFO_PANEL_SIZE, size * SQUARE_SIZE))

        pg.draw.rect(self._screen, (128, 128, 128), (0, 0, size * SQUARE_SIZE, size * SQUARE_SIZE))
        for x in range(0, size):
            for y in range(0, size):
                self._draw_square(Point(x, y), Color.BLACK)

    def _draw_square(self, position: Point, color: Color):
        (ix, iy) = position.get()
        x = ix * SQUARE_SIZE
        y = iy * SQUARE_SIZE
        pg.draw.rect(self._screen, color.value, pg.Rect(x + 1, y + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2))

    def display_info(self, world, player):
        info_labels = {
            "player_name": f"Player: {player.get_name()}",
            "score": f"Score: {world.get_score()}",
            "moves": f"Moves left: {world.get_snake().get_life()}"
        }
        pg.draw.rect(self._screen, Color.BLACK.value, pg.Rect(self._grid_size * SQUARE_SIZE, 0, self._grid_size * SQUARE_SIZE + 150, self._grid_size * SQUARE_SIZE))
        for idx, l in enumerate(info_labels):
            label = self._font.render(info_labels[l], True, Color.WHITE.value)
            self._screen.blit(label, (self._grid_size * SQUARE_SIZE + 25, (idx + 1) * 50))



    def update(self):
        pg.display.update()

    def render_snake(self, snake: List[Point]):
        self.add_snake_block(snake[0], is_head=True)
        for s in snake[1:]:
            self.add_snake_block(s)

    def render_apple(self, position: Point):
        self._draw_square(position, Color.RED)

    def remove_snake_block(self, position: Point):
        self._draw_square(position, Color.BLACK)

    def add_snake_block(self, position: Point, is_head: bool = False):
        self._draw_square(position, Color.GREEN if is_head else Color.WHITE)

    def display_game_over(self, score):
        text = [
            "GAME OVER",
            f"Your score is {score}",
            "Press ESC to quit, or any key to start new game"

        ]

        for i, line in enumerate(text):
            label = self._font.render(line, True, Color.WHITE.value)
            self._screen.blit(label, (50, i * 30))
        self.update()

__all__ = ["Renderer"]
