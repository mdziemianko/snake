from collections import namedtuple
from enum import Enum

Vector = namedtuple('Vector', ['dx', 'dy'])

class Point:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def get(self) -> (int, int):
        return self._x, self._y

    def shifted(self, v: Vector):
        return Point(self._x + v.dx, self._y + v.dy)

    def __eq__(self, other):
        return self.get() == other.get()


class Direction(Enum):
    UP = Vector(0, -1)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)
    RIGHT = Vector(1, 0)

    def is_reverse(self, other):
        v1 = self.value
        v2 = other.value
        return v1.dx == -v2.dx and v1.dy == -v2.dy
