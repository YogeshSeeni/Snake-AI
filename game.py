import pygame
from pygame.math import Vector2
from snake import Snake
from food import Food

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 30

pygame.font.init()
myfont = pygame.font.SysFont("freesansbold.ttf", 45)

pygame.display.set_caption("Snake")
window = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_grid(window):
    # Draw vertical lines
    for i in range(int(HEIGHT / GRID_SIZE)):
        pygame.draw.line(
            window,
            (255, 255, 255),
            ((i + 1) * GRID_SIZE, 0),
            ((i + 1) * GRID_SIZE, HEIGHT),
        )

    # Draw horizontal lines
    for i in range(int(WIDTH / GRID_SIZE)):
        pygame.draw.line(
            window,
            (255, 255, 255),
            (0, (i + 1) * GRID_SIZE),
            (WIDTH, (i + 1) * GRID_SIZE),
        )


def food_collision(snake, food):
    if snake.body[-1] == food.pos:
        food.reset()
        snake.insert_new()
        return True
    return False


def redraw_window(window, snake, food, score):
    window.fill((0, 0, 0))
    draw_grid(window)
    food.draw()
    snake.draw()
    draw_text(window, f"Score: {score}", (0, 0))
    pygame.display.update()


def draw_text(window, text, position):
    label = myfont.render(text, 1, (255, 255, 255))
    window.blit(label, position)


def main():

    food = Food(window, WIDTH, HEIGHT, GRID_SIZE)
    snake = Snake(window, food, WIDTH, HEIGHT, GRID_SIZE)

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