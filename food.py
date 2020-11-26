import random
import pygame
from pygame.math import Vector2


class Food:
    def __init__(self, window, WIDTH, HEIGHT, GRID_SIZE):
        self.pos = Vector2(
            random.randint(0, int(WIDTH / GRID_SIZE - 1)),
            random.randint(0, int(HEIGHT / GRID_SIZE - 1)),
        )
        self.window = window
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.GRID_SIZE = GRID_SIZE

    def draw(self):
        rect = (
            self.pos[0] * self.GRID_SIZE,
            self.pos[1] * self.GRID_SIZE,
            self.GRID_SIZE,
            self.GRID_SIZE,
        )
        pygame.draw.rect(self.window, (255, 0, 0), rect)

    def reset(self):
        self.pos = self.generate_new()

    def generate_new(self):
        return Vector2(
            random.randint(0, int(self.WIDTH / self.GRID_SIZE - 1)),
            random.randint(0, int(self.HEIGHT / self.GRID_SIZE - 1)),
        )
