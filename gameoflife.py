"""Implementation of game of life based off wikipedia"""
from blanksim import BlankSimulation

import random
import numpy as np

import tcod


class GameOfLife(BlankSimulation):
    def __init__(self) -> None:
        self.width = 128
        self.height = 72

        self.sim_buffer = np.full(
            (self.width, self.height), fill_value = False, order = "F",
        )

        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if random.randint(0,10) == 1:
                    self.sim_buffer[x, y] = True
        

    def on_update(self, dt: float) -> None:
        neighbors = 0
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                neighbors = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j ==0:
                            continue
                        else:
                            if self.sim_buffer[x + i, y + j]:
                                neighbors += 1
                if neighbors == 2:
                    continue
                elif neighbors == 3:
                    self.sim_buffer[x, y] = True
                    continue
                else:
                    self.sim_buffer[x, y] = False



    def on_render(self, console: tcod.console) -> None:
        super().on_render(console)

        # Render Buffer
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.sim_buffer[x, y]:
                    console.tiles_rgb[x, y]["bg"] = (255, 255, 255)
                