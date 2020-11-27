import pygame
from pygame.math import Vector2


class Snake:
    def __init__(self, window, food, WIDTH, HEIGHT, GRID_SIZE):
        self.body = [Vector2(5, 10), Vector2(4, 10)]
        self.direction = "RIGHT"
        self.window = window
        self.length = len(self.body)
        self.insert_block = False
        self.food = food
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.GRID_SIZE = GRID_SIZE
        self.score = 0

    def check_boundary(self, position):
        if position[0] >= 20 or position[0] < 0 or position[1] >= 20 or position[1] < 0:
            return True 
        else:
            return False

    def check_color(self, position):
        if self.window.get_at((int(position[0]*self.GRID_SIZE + 5), int(position[1]*self.GRID_SIZE) + 5)) == (0,255,0,255):
            return True 
        else:
            return False

    def return_inputs(self):
        data = []
        #LEFT
        tmp_direction = self.body[0] + Vector2(-1, 0)
        if self.check_boundary(tmp_direction) or self.check_color(tmp_direction):
            data.append(1)
        else:
            data.append(0)
        #TOP
        tmp_direction = self.body[0] + Vector2(0, -1)
        if self.check_boundary(tmp_direction) or self.check_color(tmp_direction):
            data.append(1)
        else:
            data.append(0)
        #RIGHT
        tmp_direction = self.body[0] + Vector2(1, 0)
        if self.check_boundary(tmp_direction) or self.check_color(tmp_direction):
            data.append(1)
        else:
            data.append(0)
        #DOWN
        tmp_direction = self.body[0] + Vector2(0, 1)
        if self.check_boundary(tmp_direction) or self.check_color(tmp_direction):
            data.append(1)
        else:
            data.append(0)

        data.append(self.body[0][0] / 20)
        data.append(self.body[0][1] / 20)
        data.append(self.food.pos[0] / 20)
        data.append(self.food.pos[1] / 20)
        return data
    def check_out(self):
        if (
            self.body[0][0] >= 20
            or self.body[0][1] >= 20
            or self.body[0][0] < 0
            or self.body[0][1] < 0
        ):
            return True
        return False

    def self_collision(self):
        for part in self.body[1:]:
            if part == self.body[0]:
                return True
        return False

    def insert_new(self):
        self.insert_block = True

    def draw(self):
        iteration_num = 0
        for part in self.body:
            if iteration_num == 0:
                rect = (
                    part[0] * self.GRID_SIZE,
                    part[1] * self.GRID_SIZE,
                    self.GRID_SIZE,
                    self.GRID_SIZE,
                )
                pygame.draw.rect(self.window, (0, 0, 255), rect)
                iteration_num += 1
            else:
                iteration_num += 1
                rect = (
                    part[0] * self.GRID_SIZE,
                    part[1] * self.GRID_SIZE,
                    self.GRID_SIZE,
                    self.GRID_SIZE,
                )
                pygame.draw.rect(self.window, (0, 255, 0), rect)

    def update(self):
        if self.insert_block == True:
            if self.direction == "RIGHT":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(1, 0))
                self.body = body_copy[:]

            if self.direction == "LEFT":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(-1, 0))
                self.body = body_copy[:]

            if self.direction == "UP":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(0, -1))
                self.body = body_copy[:]

            if self.direction == "DOWN":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(0, 1))
                self.body = body_copy[:]
            self.insert_block = False
            self.length = len(self.body)
        else:
            if self.direction == "RIGHT":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(1, 0))
                self.body = body_copy[:]

            if self.direction == "LEFT":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(-1, 0))
                self.body = body_copy[:]

            if self.direction == "UP":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(0, -1))
                self.body = body_copy[:]

            if self.direction == "DOWN":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(0, 1))
                self.body = body_copy[:]

            self.length = len(self.body)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.length > 1:
            if keys[pygame.K_w]:
                if self.direction != "DOWN":
                    self.direction = "UP"
            elif keys[pygame.K_a]:
                if self.direction != "RIGHT":
                    self.direction = "LEFT"
            elif keys[pygame.K_s]:
                if self.direction != "UP":
                    self.direction = "DOWN"
            elif keys[pygame.K_d]:
                if self.direction != "LEFT":
                    self.direction = "RIGHT"
        else:
            if keys[pygame.K_w]:
                self.direction = "UP"
            elif keys[pygame.K_a]:
                self.direction = "LEFT"
            elif keys[pygame.K_s]:
                self.direction = "DOWN"
            elif keys[pygame.K_d]:
                self.direction = "RIGHT"