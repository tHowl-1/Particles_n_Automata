"""Self-made fireworks implementation"""
from blanksim import BlankSimulation

from colors import doom_colors
import random
import math

from tcod import console

class Particle:
    def __init__(
        self, 
        x: float, 
        y: float, 
        vx: float, 
        vy: float, 
        color: float,
    ) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update_pos(self) -> None:
        self.x += self.vx
        self.y += self.vy


class FireWorks(BlankSimulation):
    def __init__(self) -> None:
        self.width = 128
        self.height = 72

        self.fireworks = []
        self.particles = []
        self.timer = 0.0

    def on_update(self, dt: float) -> None:
        # Update Fireworks
        random_speed = 0.0
        random_direction = 0.0
        self.timer += dt
        if self.timer > 0.1:
            self.fireworks.append(Particle(random.randint(20, self.width - 20), self.height, random.randint(-3, 3) / 10, random.randint(-18, -12) / 10, 35))
            self.timer = 0.0

        for firework in self.fireworks:
            firework.vy += 0.03
            firework.update_pos()
            if firework.vy >= 0:
                # Spawn particles and reset
                for i in range(0, 25):
                    random_speed = random.randint(5, 10) / 10
                    random_direction = (random.randint(0, 200) / 100) * math.pi
                    self.particles.append(Particle(firework.x, firework.y, random_speed * math.cos(random_direction), random_speed * math.sin(random_direction), 30 + random.randint(0, 5)))
                self.fireworks.pop(self.fireworks.index(firework))

        # Update Particles
        for particle in self.particles:
            particle.vy += 0.05
            particle.update_pos()
            particle.color -= 2.5
            if particle.color <= 0:
                self.particles.pop(self.particles.index(particle))
            


    def on_render(self, console: console) -> None:
        super().on_render(console)

        # Render Firework
        for firework in self.fireworks:
            if 0 <= firework.x < self.width and 0 <= firework.y < self.height:
                console.tiles_rgb[int(firework.x), int(firework.y)]["fg"] = doom_colors[firework.color]
                console.tiles_rgb[int(firework.x), int(firework.y)]["ch"] = ord('•')

        # Render Particles
        for particle in self.particles:
            if 0 <= particle.x < self.width and 0 <= particle.y < self.height:
                console.tiles_rgb[int(particle.x), int(particle.y)]["fg"] = doom_colors[int(particle.color)]
                console.tiles_rgb[int(particle.x), int(particle.y)]["ch"] = ord('*')
