import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (34, 139, 34)
lighty = (255, 255, 224)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Nokia Snake Game!")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Initialize hiscore
try:
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()
        if not hiscore.isdigit():
            hiscore = "0"
except FileNotFoundError:
    with open("hiscore.txt", "w") as f:
        f.write("0")
    hiscore = "0"

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(lighty)
        text_screen("Welcome to Snakes Game", black, 215, 200)
        text_screen("Press Space Bar to Play!", black, 225, 300)
        text_screen("Press Backspace to Exit!", black, 223, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("bg.mp3")
                    pygame.mixer.music.play(-1)
                    gameloop()
                if event.key == pygame.K_BACKSPACE:
                    exit_game = True

        pygame.display.update()
        clock.tick(60)


def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    global hiscore

    food_x = random.randint(20, int(screen_width / 2))
    food_y = random.randint(20, int(screen_height / 2))
    score = 0
    init_velocity = 3
    snake_size = 30
    fps = 60

    while not exit_game:
        if game_over:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("go.mp3")
            pygame.mixer.music.play(-1)  # Play game-over music once

            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Restart", black, 100, 250)
            text_screen("Press Backspace to Quit!", black, 200, 350)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Stop game-over music and restart background music
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("bg.mp3")
                        pygame.mixer.music.play(-1)
                        game_over = False
                        # Reset variables for a new game
                        snake_x, snake_y = 45, 55
                        velocity_x, velocity_y = 0, 0
                        snk_list.clear()
                        snk_length = 1
                        score = 0
                        food_x = random.randint(20, int(screen_width / 2))
                        food_y = random.randint(20, int(screen_height / 2))

                    if event.key == pygame.K_BACKSPACE:
                        exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(20, int(screen_width / 2))
                food_y = random.randint(20, int(screen_height / 2))
                snk_length += 5
                if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            text_screen("Score: " + str(score) + "  |  Hiscore: " + str(hiscore), black, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, green, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
