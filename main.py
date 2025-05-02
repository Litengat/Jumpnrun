import pygame
import sys


pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump 'n' Run Start")

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)

# Player settings
player_width = 50
player_height = 60
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0
move_speed = 5
jump_power = 15
gravity = 1
on_ground = False

# Ground
ground_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Player rectangle
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    player_vel_x = 0
    if keys[pygame.K_a]:
        player_vel_x = -move_speed
    if keys[pygame.K_d]:
        player_vel_x = move_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = -jump_power
        on_ground = False

    # Apply gravity
    player_vel_y += gravity

    # Move player
    player_rect.x += player_vel_x
    player_rect.y += player_vel_y

    # Collision with ground
    if player_rect.colliderect(ground_rect):
        player_rect.bottom = ground_rect.top
        player_vel_y = 0
        on_ground = True
    else:
        on_ground = False

    # Draw ground and player
    pygame.draw.rect(screen, GREEN, ground_rect)
    pygame.draw.rect(screen, BLUE, player_rect)

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
