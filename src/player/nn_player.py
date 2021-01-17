from player.player import Player
from world import World
from geometry import Direction, Point, Vector
import math
import numpy as np
import json

SENSORS_SIZE = 8
OUTPUT_NEURONS = 4
moves = {
    0: Direction.UP,
    1: Direction.DOWN,
    2: Direction.LEFT,
    3: Direction.RIGHT
}

class NNPlayer(Player):
    @classmethod
    def from_file(cls, path):
        with open(path, "r") as file:
            name = file.readline().rstrip("\n")
            serialized_weights = file.readline()
            weights = [np.array(a) for a in json.loads(serialized_weights)]
        return NNPlayer(weights, name)

    @classmethod
    def player(cls, layer_sizes, name):
        assert(len(layer_sizes) >= 1)
        weights = [np.random.rand(SENSORS_SIZE, layer_sizes[0]) * 2 - 1]

        for i in range(1, len(layer_sizes)):
            weights.append(np.random.rand(layer_sizes[i-1], layer_sizes[i]) * 2 - 1)

        weights.append(np.random.rand(layer_sizes[-1], OUTPUT_NEURONS) * 2 - 1)

        return NNPlayer(weights, name)

    def __init__(self, weights, name):
        self._weights = weights
        self._outputs = [0, 0, 0, 0]
        self._name = name

    def to_file(self, path):
        serialized_weights = json.dumps([a.tolist() for a in  self._weights])
        with open(path, "w") as file:
            file.write(self._name)
            file.write("\n")
            file.write(serialized_weights)

    def cross(self, other):
        def do_cross(a, b):
            mask = np.random.rand(*a.shape) > 0.5
            return a * mask + b * (1 - mask)

        assert(len(self._weights) == len(other._weights))

        weights = []
        for i in range(0, len(self._weights)):
            assert(self._weights[i].shape == other._weights[i].shape)
            weights.append(do_cross(self._weights[i], other._weights[i]))

        return NNPlayer(weights)

    def with_name(self, name):
        self._name = name
        return self

    def mutate(self, probability):
        def do_mutation(v):
            mask = np.random.rand(*v.shape) < probability
            return ((np.random.rand(*v.shape) * 2 - 1) * mask) + v * (1 - mask)

        weights = []
        for w in self._weights:
            weights.append(do_mutation(w))

        return NNPlayer(weights, self._name)

    def get_name(self) -> str:
        return self._name

    def _forward(self, senses):
        assert (len(senses) == len(self._weights[0]))

        state = senses
        for w in self._weights:
            state = _activation(state, w)

        return state


    def _look(self, world: World, position: Point, direction: Vector):
        point = position.shifted(direction)
        see_apple = False
        i = 1
        while (point._x < World.size and point._x >= 0 and point._y < World.size and point._y >= 0):
            if (world._apple_position == point):
                see_apple = True
            if world.has_snake(point):
                return (see_apple, i)
            point = point.shifted(direction)
            i = i + 1
        return (see_apple, i)


    def _sense(self, world: World):
        def to_vals(view):
            (has_apple, distance_to_obstacle) = view
            return [1 if has_apple else 0, 1.0/ distance_to_obstacle]

        head_position = world._snake.head()
        look_left = self._look(world, head_position, Direction.LEFT.value)
        look_right = self._look(world, head_position, Direction.RIGHT.value)
        look_up = self._look(world, head_position, Direction.UP.value)
        look_down = self._look(world, head_position, Direction.DOWN.value)

        return np .array(
            to_vals(look_left) + to_vals(look_right) + to_vals(look_up) + to_vals(look_down)
        )


        #direction = world._snake._direction.value

        #apple_position = world._apple_position.get()

        #d = round(math.sqrt(math.pow(head_position[0] - apple_position[0], 2) + math.pow(head_position[1] - apple_position[1], 2)),2)

        # look_left = 30
        # for i in range(1, 30):
        #     x = head_position[0] - i
        #     if x <= 0 or has_snake((x, head_position[1])):
        #         look_left = i
        #         break
        #
        # look_right = 30
        # for i in range(1, 30):
        #     x = head_position[0] + i
        #     if x >= World.size - 1 or has_snake((x, head_position[1])):
        #         look_right = i
        #         break
        #
        # look_up = 30
        # for i in range(1, 30):
        #     y = head_position[1] - i
        #     if y <= 0 or has_snake((head_position[0], y)):
        #         look_up = i
        #         break
        #
        # look_down = 30
        # for i in range(1, 30):
        #     y = head_position[1] + i
        #     if y >= World.size - 1 or has_snake((head_position[0], y)):
        #         look_down = i
        #         break
        #
        # ax = (apple_position[0] - head_position[0])/ (World.size + 1)
        # ay = (apple_position[1] - head_position[1]) / (World.size + 1)
        # return np.array([
        #    direction.dx/ 30, direction.dy / 30,
        #     # 1 if direction.dx == 1 else 0, 1 if direction.dx == -1 else 0,
        #     # 1 if direction.dy == 1 else 0, 1 if direction.dy == -1 else 0,
        #    # d / (World.size * 1.41),
        #     ax, ay,
        #     look_left / (World.size + 1),
        #     look_right  / (World.size + 1),
        #     look_up / (World.size + 1),
        #     look_down  / (World.size + 1),
        #    # head_position[0]/ (World.size + 1),
        #    #  head_position[1] / (World.size + 1),
        #    # (World.size - head_position[0] - 1)/  (World.size - 1),
        #    #  (World.size - head_position[1] - 1) / (World.size - 1)
        # ])


    def get_direction(self, world: World) -> Direction:
        senses = self._sense(world)
        outputs = self._forward(senses)
        move = outputs.argmax()
        self._outputs = list(outputs)
        return moves[move]

    def get_speed(self):
        return 50



def _activation(inputs, weights):
    z = np.dot(inputs, weights)#.sum(axis=1)
    return np.vectorize(math.tanh)(z)