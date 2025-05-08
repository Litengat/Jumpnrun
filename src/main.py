import pygame
import sys

from Player import Player
from object import Object


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

move_speed = 5
jump_power = 15
gravity = 1
on_ground = False

# Ground
ground_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

# Player rectangle
# Calculate initial player position
initial_player_x = 50  # Example starting X
initial_player_y = HEIGHT - 50 - player_height  # Start on top of the ground


objects = []


# player = Player() # Old instantiation
player = Player(initial_player_x, initial_player_y, player_width, player_height, BLUE) # New instantiation


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
    player.vel_x = 0
    if keys[pygame.K_a]:
        player.vel_x = -move_speed
    if keys[pygame.K_d]:
        player.vel_x = move_speed
    if keys[pygame.K_SPACE] and on_ground:
        player.vel_y = -jump_power
        on_ground = False

    # Apply gravity
    player.vel_y += gravity

    # Move player
    player.rect.x += player.vel_x
    player.rect.y += player.vel_y

    # Collision with ground
    if player.rect.colliderect(ground_rect):
        player.rect.bottom = ground_rect.top
        player.vel_y = 0
        on_ground = True
    else:
        on_ground = False


    for obj in objects:
        obj.render(screen)
    
    # Draw ground and player
    pygame.draw.rect(screen, GREEN, ground_rect)
    # pygame.draw.rect(screen, BLUE, player_rect) # Old, problematic drawing
    player.render(screen) # Use the player's draw method
    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
