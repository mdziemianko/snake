
import random
import numpy as np

random.seed(34)
np.random.seed(42)

import pygame as pg
from world import World
from renderer import Renderer
from geometry import *
from player import NNPlayer, Player
import math
from world.game import Game

import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


SNAKES_PER_GENERATION = 500


def run():
    generation = 1
    best_score = 0
    best_fitness = 0
    best_snake = None

    renderer = Renderer(50)

    snakes = [NNPlayer.player([30, 15], f"NNet_{generation}_{i}") for i in range(SNAKES_PER_GENERATION)]

    should_quit = False

    while not should_quit:
        logger.info("Generation %s", generation)
        snakes_with_score = run_simulations(snakes)

        logger.info("generation %s best fitness is %s", generation, round(snakes_with_score[0][1], 2))
        logger.debug("fitness  quantiles: %s", [round(snakes_with_score[x][1], 2) for x in range(0, SNAKES_PER_GENERATION, SNAKES_PER_GENERATION //10)])

        if snakes_with_score[0][1] > best_fitness:
            best_fitness = snakes_with_score[0][1]

            if snakes_with_score[0][0] != best_snake:
                best_snake = snakes_with_score[0][0]
                best_snake.to_file(f"./{best_snake.get_name()}.snk")
                score = show_run(best_snake, renderer)

                if score > best_score:
                    logger.info(f"New best score is {score}")
                    best_score = score

        generation = generation + 1
        snakes = breed(snakes_with_score, generation)


def run_simulations(snakes):
    logger.info("Simulating %s snakes...", len(snakes))
    snakes_with_score = []
    for idx, s in enumerate(snakes):
        world = World()
        game = Game(world, s)
        game.play()
        fitness = evaluate(world)
        result = (s, fitness)
        snakes_with_score.append(result)

    return sorted(snakes_with_score, key=lambda x: -x[1])


def show_run(snake, renderer):
    world = World()
    game = Game(world, snake, renderer)
    game.play()
    return world.get_score()


def breed(snakes, generation):
    top_snakes = snakes[0:(len(snakes) // 10)]
    #new_snakes =  [s[0] for s in top_snakes] + [s[0].cross(random.choice(top_snakes)[0]).mutate(p) for s in top_snakes for p in [0.01, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.2]]
    new_snakes = [s[0] for s in top_snakes] + [s[0].mutate(p).with_name(f"NNet_{generation}_{i}") for i, s in enumerate(top_snakes) for p in [0.01, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.2]]
    return new_snakes


def evaluate(world):
    return math.pow(2, math.log2(world.get_score() + 1)) * math.log2(world.get_score() + 1)


def wait() -> bool:
    while True:
        event = pg.event.wait()
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            return True
        elif event.type == pg.KEYDOWN:
            return False


if __name__ == "__main__":
    run()