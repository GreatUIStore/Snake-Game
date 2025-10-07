import pygame
import random
import sys
import os

pygame.init()
LIGHT_GREEN_1 = (170, 215, 81)
LIGHT_GREEN_2 = (162, 209, 73)
SNAKE_BLUE = (0, 102, 204)
APPLE_RED = (255, 0, 0)
APPLE_LEAF_GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20
clock = pygame.time.Clock()
FPS = 10
font = pygame.font.SysFont(None, 35)
small_font = pygame.font.SysFont(None, 25)
HIGH_SCORE_FILE = 'high_score.txt'

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as f:
            try:
                val = int(f.read().strip())
                if val < 0:
                    return 0
                return val
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

def draw_background():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_GREEN_1, rect)
            else:
                pygame.draw.rect(screen, LIGHT_GREEN_2, rect)

def draw_snake(snake_body):
    for block in snake_body:
        rect = pygame.Rect(block[0], block[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, SNAKE_BLUE, rect)

def draw_food(food_pos):
    center = (food_pos[0] + BLOCK_SIZE // 2, food_pos[1] + BLOCK_SIZE // 2)
    radius = BLOCK_SIZE // 2 - 4
    pygame.draw.circle(screen, APPLE_RED, center, radius)
    leaf_points = [
        (center[0], center[1] - radius),
        (center[0] + 3, center[1] - radius - 6),
        (center[0] + 6, center[1] - radius + 1)
    ]
    pygame.draw.polygon(screen, APPLE_LEAF_GREEN, leaf_points)

def draw_score(score, high_score):
    score_text = small_font.render(f"Score: {score}", True, BLACK)
    high_score_text = small_font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

def draw_end_screen(score, high_score, button_rect):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  
    screen.blit(overlay, (0, 0))

    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 3 + 50))

    pygame.draw.rect(screen, SNAKE_BLUE, button_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
    button_text = font.render("Play Again", True, WHITE)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))

def game_loop():
    high_score = load_high_score()
    game_over = False
    game_close = False

    x1 = WIDTH // 2
    y1 = HEIGHT // 2

    x1_change = BLOCK_SIZE
    y1_change = 0

    snake_body = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    score = 0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        draw_background()

        snake_head = [x1, y1]
        snake_body.append(snake_head)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        for x in snake_body[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_body)
        draw_food([foodx, foody])
        draw_score(score, high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1
            score += 1

        clock.tick(FPS)

        if game_close:
            if score > high_score:
                high_score = score
                save_high_score(high_score)

            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            draw_end_screen(score, high_score, button_rect)
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        game_over = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            waiting = False
                            game_close = False

                            x1 = WIDTH // 2
                            y1 = HEIGHT // 2
                            x1_change = BLOCK_SIZE
                            y1_change = 0
                            snake_body = []
                            length_of_snake = 1
                            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                            score = 0

    pygame.quit()
    sys.exit()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

game_loop()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

game_loop()
