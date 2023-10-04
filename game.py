import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
ROCKET_WIDTH = 80
ROCKET_HEIGHT = 20
BALL_RADIUS = 5
ROCKET_SPEED = 5
BALL_SPEED = 10
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Ball Game")

def initialize_game():
    global rocket_x, rocket_y, ball_x, ball_y, ball_speed_x, ball_speed_y, game_over

    rocket_x = (SCREEN_WIDTH - ROCKET_WIDTH) // 2
    rocket_y = SCREEN_HEIGHT - ROCKET_HEIGHT

    ball_x = random.randint(0, SCREEN_WIDTH - BALL_RADIUS)
    ball_y = 0
    ball_speed_y = BALL_SPEED
    ball_speed_x = 0

    game_over = False

initialize_game()

def calculate_bounce_angle(rocket_x, rocket_width, ball_x):
    relative_intersect_x = (rocket_x + rocket_width / 2) - (ball_x + BALL_RADIUS)
    normalized_relative_intersect_x = relative_intersect_x / (rocket_width / 2)
    bounce_angle = normalized_relative_intersect_x * (math.pi / 2)  # Adjust the bounce angle as needed
    return bounce_angle

# Clock to control frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and rocket_x > 0:
            rocket_x -= ROCKET_SPEED
        if keys[pygame.K_RIGHT] and rocket_x < SCREEN_WIDTH - ROCKET_WIDTH:
            rocket_x += ROCKET_SPEED

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > SCREEN_WIDTH:
            ball_speed_x *= -1

        if ball_y - BALL_RADIUS < 0:
            ball_speed_y *= -1

        if (
            rocket_x < ball_x < rocket_x + ROCKET_WIDTH
            and rocket_y < ball_y < rocket_y + ROCKET_HEIGHT
        ):
            bounce_angle = calculate_bounce_angle(rocket_x, ROCKET_WIDTH, ball_x)
            ball_speed_x = BALL_SPEED * math.sin(bounce_angle)
            ball_speed_y = BALL_SPEED * -math.cos(bounce_angle)

        if ball_y + BALL_RADIUS > SCREEN_HEIGHT:
            game_over = True

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            initialize_game()

    screen.fill(BLACK)

    pygame.draw.rect(screen, RED, (rocket_x, rocket_y, ROCKET_WIDTH, ROCKET_HEIGHT))

    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Press 'R' to Restart", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
