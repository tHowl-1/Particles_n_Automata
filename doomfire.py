"""Implementation of doom fire from fabiensanglard.net"""
from blanksim import BlankSimulation

from colors import doom_colors
import random
import numpy as np

from tcod import console


class DoomFire(BlankSimulation):
    def __init__(self) -> None:
        self.width = 128
        self.height = 72

        self.sim_buffer = np.full(
            (self.width, self.height), fill_value = 0, order = "F",
        )

        self.sim_buffer[0: self.width - 0, self.height - 1] = 35
        
    def on_update(self, dt: float) -> None:
        for x in range(0, self.width):
            for y in range(1, self.height):
                self.sim_buffer[min(self.width - 1, max(0, x + random.randint(-1, 1))), y - 1] = max(0, self.sim_buffer[x, y] + random.randint(-2, 0))

    def on_render(self, console: console) -> None:
        super().on_render(console)

        # Render Buffer
        for x in range(0, self.width):
            for y in range(0, self.height):
                console.tiles_rgb[x, y]["bg"] = doom_colors[self.sim_buffer[x, y]]
                