import pygame
from pygame.math import Vector2
from snake import Snake
from food import Food
import neat
import os

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


def redraw_window(window, snakes, food, score):
    window.fill((0, 0, 0))
    draw_grid(window)
    food.draw()
    for snake in snakes:
        snake.draw()
    draw_text(window, f"Score: {score}", (0, 0))
    pygame.display.update()


def draw_text(window, text, position):
    label = myfont.render(text, 1, (255, 255, 255))
    window.blit(label, position)

gen = 0
def main(genomes, config):
    global gen 
    gen += 1

    food = Food(window, WIDTH, HEIGHT, GRID_SIZE)

    nets = []
    snakes = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        # Init my cars
        snakes.append(Snake(window, food, WIDTH, HEIGHT, GRID_SIZE))

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    score = 0
    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for index, snake in enumerate(snakes):
            output = nets[index].activate(snake.return_inputs())
            i = output.index(max(output))
            print(i)
            if i == 0:
                snake.direction = "LEFT"
            if i == 1:
                snake.direction = "UP"
            if i == 2:
                snake.direction = "RIGHT"
            else:
                snake.direction = "DOWN"

        remain_snakes = 0
        for i, snake in enumerate(snakes):
            if snake.self_collision() == False and snake.check_out() == False:
                remain_snakes += 1
                for event in pygame.event.get():
                    snake.update()
                genomes[i][1].fitness += snake.score

        if remain_snakes == 0:
            break
        # snake.move()

        # if snake.self_collision() or snake.check_out():
        #     running = False

        for snake in snakes:
            if food_collision(snake, food):
                snake.score += 1

        # snake.return_inputs()
        redraw_window(window, snakes, food, score)
        clock.tick(30)


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)