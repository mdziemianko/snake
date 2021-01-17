import random
from geometry import *
from typing import List

WORLD_SIZE = 30
LIFE_TIME = WORLD_SIZE * WORLD_SIZE // 2

class Snake:
    def __init__(self, initial_size: int = 5, direction : Direction = Direction.DOWN, head: Point = Point(0, 0)):
        self._direction = direction
        shift = direction.value
        self._body = [head.shifted((lambda x: Vector(shift.dx * -i, shift.dy * -i))(i)) for i in range(0, initial_size)]
        self._vacated = None
        self._life_left = LIFE_TIME

    def get_life(self):
        return self._life_left

    def is_alive(self):
        return self._life_left > 0

    def move(self):
        self._body.insert(0, self._body[0].shifted(self._direction.value))
        self._vacated = self._body.pop()
        self._life_left = self._life_left - 1

    def grow(self):
        self._body.append(self._vacated)
        self._vacated = None
        self._life_left = LIFE_TIME

    def head(self) -> Point:
        return self._body[0]

    def get_size(self):
        return len(self._body)

    def get_body(self) -> List[Point]:
        return self._body

    def get_vacated(self):
        return self._vacated

    def set_direction(self, direction: Direction):
        if direction is not None: # and not direction.is_reverse(self._direction):
            self._direction = direction

class World:
    size = WORLD_SIZE
    apples = random.sample([Point(x, y) for x in range(WORLD_SIZE) for y in range(WORLD_SIZE)], WORLD_SIZE * WORLD_SIZE)

    def __init__(self, initial_snake_size = 5):
        self._initial_snake_size = initial_snake_size
        self._epoch = 0
        self._snake = Snake()

        self._apple_id = 0
        self._apple_position = self._create_apple()

    def _create_apple(self) -> Point:
        self._apple_id = self._apple_id + 1
        while self.has_snake(self.apples[self._apple_id]):
            self._apple_id = self._apple_id + 1
        return self.apples[self._apple_id]

    def is_collision(self):
        head = self._snake.head().shifted(self._snake._direction.value)
        (x, y) = head.get()
        boundry = x < 0 or x >= World.size or y < 0 or y >= World.size
        body = len([s for s in self._snake.get_body()[1:] if s == head]) > 0
        return boundry or body

    def check_apple(self):
        return self._snake.head() == self._apple_position

    def get_apple_position(self) -> Point:
        return self._apple_position

    def get_score(self):
        return self._snake.get_size() - self._initial_snake_size

    def evolve(self):
        collision = self.is_collision()

        if not collision:
            self._snake.move()

            if self.check_apple():
                self._apple_position = self._create_apple()
                self._snake.grow()

            self._epoch = self._epoch + 1

        return not collision and self._snake.is_alive()

    def has_snake(self, point: Point):
        for s in self._snake.get_body():
            if (s == point):
                return True
        return False

    def get_snake(self):
        return self._snake

