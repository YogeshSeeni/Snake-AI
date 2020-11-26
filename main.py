import pygame
from pygame.math import Vector2
import random
import neat

class Snake:
    def __init__(self, window, food):
        self.body = [Vector2(5,10),Vector2(4,10)]
        self.direction = "RIGHT"
        self.window = window
        self.length = len(self.body)
        self.insert_block = False
        self.food = food

    def check_out(self):
        if self.body[0][0] > 20 or self.body[0][1] > 20 or self.body[0][0] < 0 or self.body[0][1] < 0:
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
                rect = (part[0]*GRID_SIZE, part[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.window, (0,0,255), rect)
                iteration_num +=1
            else:
                iteration_num += 1
                rect = (part[0]*GRID_SIZE, part[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.window, (0,255,0), rect)
    
    def update(self):
        if self.insert_block == True:
            if self.direction == "RIGHT":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(1,0))
                self.body = body_copy[:]
            
            if self.direction == "LEFT":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(-1,0))
                self.body = body_copy[:]

            if self.direction == "UP":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(0,-1))
                self.body = body_copy[:]

            if self.direction == "DOWN":
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + Vector2(0,1))
                self.body = body_copy[:]
            self.insert_block = False
            self.length = len(self.body)
        else:
            if self.direction == "RIGHT":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(1,0))
                self.body = body_copy[:]

            if self.direction == "LEFT":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(-1,0))
                self.body = body_copy[:]

            if self.direction == "UP":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(0,-1))
                self.body = body_copy[:]

            if self.direction == "DOWN":
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + Vector2(0,1))
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

        

class Food:
    def __init__(self, window):
        self.pos = Vector2(random.randint(0,int(WIDTH/GRID_SIZE - 1)),random.randint(0,int(HEIGHT/GRID_SIZE - 1)))
        self.window = window

    def draw(self):
        rect = (self.pos[0] * GRID_SIZE, self.pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.window, (255, 0, 0), rect)

    def reset(self):
        self.pos = self.generate_new()

    def generate_new(self):
        return Vector2(random.randint(0,int(WIDTH/GRID_SIZE - 1)),random.randint(0,int(HEIGHT/GRID_SIZE - 1)))

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 30

pygame.font.init()
myfont = pygame.font.SysFont('freesansbold.ttf', 45)

pygame.display.set_caption("Snake")
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_grid(window):
    #Draw vertical lines
    for i in range(int(HEIGHT/GRID_SIZE)):
        pygame.draw.line(window, (255,255,255), ((i+1) * GRID_SIZE, 0), ((i+1) * GRID_SIZE, HEIGHT))
    
    #Draw horizontal lines
    for i in range(int(WIDTH/GRID_SIZE)):
        pygame.draw.line(window, (255,255,255), (0, (i+1) * GRID_SIZE), (WIDTH, (i+1) * GRID_SIZE))

def food_collision(snake, food):
    if snake.body[-1] == food.pos:
        food.reset()
        snake.insert_new()
        return True
    return False

def redraw_window(window, snake, food, score):
    window.fill((0,0,0))
    draw_grid(window)
    food.draw()
    snake.draw()
    draw_text(window, f"Score: {score}", (0,0))
    pygame.display.update()

def draw_text(window, text, position):
    label = myfont.render(text, 1, (255,255,255))
    window.blit(label, position)

def main():

    food = Food(window)
    snake = Snake(window, food)

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    score = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SCREEN_UPDATE:
                snake.update()
        

        snake.move()

        if snake.self_collision() or snake.check_out():
            running = False
        if food_collision(snake, food):
            score += 1
        
        redraw_window(window, snake, food, score)
        clock.tick(60)
        

main()