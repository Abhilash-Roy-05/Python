import pygame
import random
import os

pygame.init()

# ================== SETTINGS ==================
WIDTH, HEIGHT = 600, 400
BLOCK = 20
BASE_SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# ================== COLORS ==================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)

# ================== FONTS ==================
font_small = pygame.font.SysFont("comicsansms", 25)
font_big = pygame.font.SysFont("comicsansms", 40)

# ================== HIGH SCORE ==================
HIGHSCORE_FILE = "highscore.txt"

def get_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write("0")
    with open(HIGHSCORE_FILE, "r") as f:
        return int(f.read())

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# ================== UI FUNCTIONS ==================
def show_text(msg, color, y_offset=0, big=False):
    font = font_big if big else font_small
    text = font.render(msg, True, color)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(text, rect)

def draw_score(score, level, highscore):
    text = font_small.render(
        f"Score: {score}   Level: {level}   High Score: {highscore}",
        True, YELLOW
    )
    screen.blit(text, (10, 10))

# ================== START SCREEN ==================
def start_screen():
    waiting = True
    while waiting:
        screen.fill(BLACK)
        show_text("🐍 Snake Game", GREEN, -40, big=True)
        show_text("Press SPACE to Start", WHITE, 10)
        show_text("Arrow Keys to Move", WHITE, 40)
        show_text("ESC to Quit", WHITE, 70)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# ================== GAME OVER SCREEN ==================
def game_over_screen(score, highscore):
    waiting = True
    while waiting:
        screen.fill(BLACK)
        show_text("Game Over", RED, -40, big=True)
        show_text(f"Your Score: {score}", WHITE, 10)
        show_text(f"High Score: {highscore}", WHITE, 40)
        show_text("Press R to Restart or ESC to Quit", WHITE, 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# ================== MAIN GAME ==================
def game_loop():
    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0

    snake = []
    length = 1

    food_x = random.randrange(0, WIDTH, BLOCK)
    food_y = random.randrange(40, HEIGHT, BLOCK)

    score = 0
    level = 1
    speed = BASE_SPEED

    highscore = get_highscore()

    # Load background
    background_img = None
    try:
        background_img = pygame.image.load("background.png")
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT - 40))
    except Exception as e:
        print(f"Could not load background: {e}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -BLOCK; dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = BLOCK; dy = 0
                elif event.key == pygame.K_UP:
                    dy = -BLOCK; dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = BLOCK; dx = 0

        x += dx
        y += dy

        # Wall collision
        if x < 0 or x >= WIDTH or y < 40 or y >= HEIGHT:
            running = False

        screen.fill(BLACK)

        # Draw background or fill black
        if background_img:
            screen.blit(background_img, (0, 40))

        # Draw borders
        pygame.draw.rect(screen, WHITE, (0, 40, WIDTH, HEIGHT - 40), 3)

        # Draw food
        pygame.draw.rect(screen, RED, (food_x, food_y, BLOCK, BLOCK))

        head = [x, y]
        snake.append(head)

        if len(snake) > length:
            del snake[0]

        # Self collision
        for part in snake[:-1]:
            if part == head:
                running = False

        # Draw snake
        for part in snake:
            pygame.draw.rect(screen, GREEN, (part[0], part[1], BLOCK, BLOCK))

        # Food collision
        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH, BLOCK)
            food_y = random.randrange(40, HEIGHT, BLOCK)
            length += 1
            score += 10

            # Level up every 50 points
            if score % 50 == 0:
                level += 1
                speed += 2

        # High score update
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        draw_score(score, level, highscore)

        pygame.display.update()
        clock.tick(speed)

    game_over_screen(score, highscore)

# ================== MAIN ==================
while True:
    start_screen()
    game_loop()
