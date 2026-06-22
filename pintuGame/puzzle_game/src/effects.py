import math
import random

import pygame


class ParticleBurst:
    def __init__(self):
        self.particles = []

    def burst(self, center, count=80):
        palette = [(238, 190, 96), (75, 189, 180), (234, 111, 91), (102, 184, 128)]
        rng = random.Random()
        for _ in range(count):
            angle = rng.random() * math.tau
            speed = rng.uniform(1.2, 5.2)
            self.particles.append(
                {
                    "x": float(center[0]),
                    "y": float(center[1]),
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed - rng.uniform(0.4, 1.6),
                    "life": rng.uniform(0.6, 1.4),
                    "color": rng.choice(palette),
                    "radius": rng.uniform(2.5, 5.5),
                }
            )

    def update(self, dt):
        alive = []
        for p in self.particles:
            p["life"] -= dt
            if p["life"] > 0:
                p["vy"] += 5.5 * dt
                p["x"] += p["vx"] * 60 * dt
                p["y"] += p["vy"] * 60 * dt
                alive.append(p)
        self.particles = alive

    def draw(self, surface):
        for p in self.particles:
            alpha = max(0, min(255, int(255 * p["life"])))
            radius = max(1, int(p["radius"]))
            temp = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(temp, (*p["color"], alpha), (radius * 2, radius * 2), radius)
            surface.blit(temp, (p["x"] - radius * 2, p["y"] - radius * 2))
