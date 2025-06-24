import os
import random
import math
import pygame



pygame.init()

pygame.display.set_caption("Jump n run")

WIDTH, HEIGHT = 1280, 720

FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


from traps.FallingPlatform import FallingPlatform
from traps.Saw import Saw
from traps.Fan import Fan
from os import listdir
from os.path import isfile, join

from block import Block
from fire import Fire
from player import Player
from level_loader import load_level










def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x,offset_y):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        if(isInScreen(obj,offset_x,offset_y)):
            obj.draw(window, offset_x,offset_y)

    player.draw(window, offset_x,offset_y)

    pygame.display.update()

def isInScreen(obj, offset_x, offset_y):
    x = obj.rect.x - offset_x
    y = obj.rect.y - offset_y
    if x > WIDTH * 1.5 or y > HEIGHT * 1.5 or x < -100 or y < -100:
        return False
    return True

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if obj.collide(player):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        collide = obj.collide(player)
        if collide:
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2) # objects die left colliden 
    collide_right = collide(player, objects, PLAYER_VEL * 2)# objects die right colliden 

    if keys[pygame.K_a] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.death()





def draw_death_screen(window):
    #  semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(10)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))
    
    # Fonts 
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    instruction_font = pygame.font.SysFont("Arial", 36)
    
    # Game Over text
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    window.blit(game_over_text, game_over_rect)
    
    # Instructions
    retry_text = instruction_font.render("Press R to Retry", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(retry_text, retry_rect)
    
    menu_text = instruction_font.render("Press Q or ESC to Return to Menu", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    window.blit(menu_text, menu_rect)
    
    pygame.display.update()

def reset_game(level_name="level"):
    """Reset the game to initial state"""
    player = Player(100, 100, 50, 50)
    player.DEATH = False
    objects = load_level(level_name)
    offset_x = 0
    offset_y = 0
    return player, objects, offset_x, offset_y

def get_available_levels():
    """Get list of available level files"""
    levels_dir = "levels"
    levels = []
    if os.path.exists(levels_dir):
        for file in os.listdir(levels_dir):
            if file.endswith('.json'):
                level_name = file[:-5]  # Remove .json extension
                levels.append(level_name)
    return sorted(levels)

def draw_menu(window, background, bg_image, selected_level, available_levels):
    """Draw the main menu"""
    # Draw background
    for tile in background:
        window.blit(bg_image, tile)
    
    # Fonts
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    level_font = pygame.font.SysFont("Arial", 48)
    instruction_font = pygame.font.SysFont("Arial", 32)
    
    # Title
    title_text = title_font.render("JUMP N RUN", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    window.blit(title_text, title_rect)
    
    # Level selection
    level_title = level_font.render("Select Level:", True, (255, 255, 255))
    level_title_rect = level_title.get_rect(center=(WIDTH // 2, 200))
    window.blit(level_title, level_title_rect)
    
    # Draw level options
    start_y = 280
    for i, level in enumerate(available_levels):
        color = (255, 255, 0) if i == selected_level else (255, 255, 255)
        level_text = level_font.render(f"{i + 1}. {level}", True, color)
        level_rect = level_text.get_rect(center=(WIDTH // 2, start_y + i * 60))
        window.blit(level_text, level_rect)
    
    # Instructions
    instructions = [
        "Use UP/DOWN arrows to select level",
        "Press ENTER to start",
        "Press ESC to quit"
    ]
    
    for i, instruction in enumerate(instructions):
        inst_text = instruction_font.render(instruction, True, (200, 200, 200))
        inst_rect = inst_text.get_rect(center=(WIDTH // 2, HEIGHT - 150 + i * 40))
        window.blit(inst_text, inst_rect)
    
    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    # Game states
    MENU = "menu"
    GAME = "game"
    current_state = MENU
    
    # Menu variables
    available_levels = get_available_levels()
    selected_level_index = 0
    current_level_name = available_levels[0] if available_levels else "level"
    
    # Game variables
    block_size = 96
    player = None
    objects = []
    offset_x = 0
    offset_y = 0
    scroll_area_width = 200

    run = True

    while run:
        dt = clock.tick(FPS) / 10
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if current_state == MENU:
                    # Menu navigation
                    if event.key == pygame.K_UP:
                        selected_level_index = (selected_level_index - 1) % len(available_levels)
                    elif event.key == pygame.K_DOWN:
                        selected_level_index = (selected_level_index + 1) % len(available_levels)
                    elif event.key == pygame.K_RETURN:
                        # Start selected level
                        current_level_name = available_levels[selected_level_index]
                        player, objects, offset_x, offset_y = reset_game(current_level_name)
                        current_state = GAME
                    elif event.key == pygame.K_ESCAPE:
                        run = False
                        break
                        
                elif current_state == GAME:
                    if player.DEATH:
                        # Handle death screen inputs
                        if event.key == pygame.K_r:
                            # Retry the current level
                            player, objects, offset_x, offset_y = reset_game(current_level_name)
                        elif event.key == pygame.K_q:
                            # Return to menu
                            current_state = MENU
                        elif event.key == pygame.K_ESCAPE:
                            # Return to menu
                            current_state = MENU
                    else:
                        # Normal game inputs
                        if event.key == pygame.K_SPACE and player.jump_count < 2:
                            player.jump()
                        elif event.key == pygame.K_ESCAPE:
                            # Return to menu
                            current_state = MENU

        if current_state == MENU:
            # Draw menu
            draw_menu(window, background, bg_image, selected_level_index, available_levels)
            
        elif current_state == GAME:
            # Check for fall death
            if player.rect.y >= 1000:
                player.death()

            # If player is dead, show death screen
            if player.DEATH:
                draw_death_screen(window)
                continue

            # Update game objects
            for obj in objects:
                obj.loop()
            player.loop(FPS, dt)

            # Handle player movement
            handle_move(player, objects)
            
            # Update camera
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

            if ((player.rect.top - offset_y >= HEIGHT - scroll_area_width) and player.y_vel > 0) or (
                    (player.rect.bottom - offset_y <= scroll_area_width) and player.y_vel < 0):
                offset_y += player.y_vel

            # Draw game
            draw(window, background, bg_image, player, objects, offset_x, offset_y)

            # Draw FPS
            font = pygame.font.SysFont("Verdana", 20)
            fps_text = font.render(str(round(clock.get_fps(), 2)), True, (255, 255, 255))
            window.blit(fps_text, (10, 10))
            pygame.display.update()

    pygame.quit()
    quit()



if __name__ == "__main__":
    main(window)
