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
from finish import Finish
from player import Player
from level_loader import load_level
from sprites import load_sprite_sheets
from completion_tracker import CompletionTracker
from menu import MenuHandler, draw_death_screen, draw_level_completion_ui

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
    if x > WIDTH * 2 or y > HEIGHT * 2 or x < -WIDTH or y < -HEIGHT:
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

    # level_completed = False
    #     elif obj and obj.name == "finish":
    #         # Player reached finish line
    #         if obj.activate():  # Only trigger once
    #             # Trigger confetti from screen corners towards finish line
    #             confetti_system.trigger(obj.rect.centerx, obj.rect.centery, 70)
    #             # Mark level as completed
    #             completion_tracker.mark_completed(current_level_name)
    #             level_completed = True
    #             print(f"Level {current_level_name} completed!")
    
    # return level_completed





def reset_game(level_name="level"):
    """Reset the game to initial state"""
    player = Player(0, HEIGHT - 96, 50, 50)
    player.WINNING = False
    player.DEATH = False
    objects = load_level(level_name)
    offset_x = 0
    offset_y = 0
    return player, objects, offset_x, offset_y

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    # Game states
    MENU = "menu"
    GAME = "game"
    current_state = MENU
    
    # Initialize systems
    completion_tracker = CompletionTracker()
    menu_handler = MenuHandler()
    
    # Menu variables
    current_level_name = menu_handler.get_current_level_name()
    
    # Game variables
    block_size = 96
    player = None
    objects = []
    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    level_completed = False

    run = True

    while run:
        dt = clock.tick(FPS) / 10
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if current_state == MENU:
                    # Menu navigation (slideshow style)
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        menu_handler.navigate_left()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        menu_handler.navigate_right()
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Start selected level
                        current_level_name = menu_handler.get_current_level_name()
                        player, objects, offset_x, offset_y = reset_game(current_level_name)
                        level_completed = False
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
                            level_completed = False
                        elif event.key == pygame.K_q:
                            # Return to menu
                            current_state = MENU
                        elif event.key == pygame.K_ESCAPE:
                            # Return to menu
                            current_state = MENU
                    elif player.WINNING:
                        completion_tracker.mark_completed(current_level_name)
                        current_state = MENU

                    else:
                        # Normal game inputs
                        if event.key == pygame.K_SPACE and player.jump_count < 2:
                            player.jump()
                        elif event.key == pygame.K_ESCAPE:
                            # Return to menu
                            current_state = MENU
                        elif event.key == pygame.K_n and level_completed:
                            # Go to next level if available
                            current_level_name = menu_handler.go_to_next_level()
                            player, objects, offset_x, offset_y = reset_game(current_level_name)
                            level_completed = False
                    

        if current_state == MENU:
            # Draw slideshow menu
            menu_handler.draw(window, background, bg_image, completion_tracker)
            
        elif current_state == GAME:
            # Update confetti system
            
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

            # Handle player movement and check for level completion
            if not level_completed:
                level_completed = handle_move(player, objects)
            
            # Update camera
            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

            if ((player.rect.top - offset_y >= HEIGHT - scroll_area_width) and player.y_vel > 0) or (
                    (player.rect.bottom - offset_y <= scroll_area_width) and player.y_vel < 0):
                offset_y += player.y_vel

            # Draw game
            draw(window, background, bg_image, player, objects, offset_x, offset_y)
            
            # Show level completion message
            if level_completed:
                draw_level_completion_ui(window)

            # Draw FPS
            font = pygame.font.SysFont("Verdana", 20)
            fps_text = font.render(str(round(clock.get_fps(), 2)), True, (255, 255, 255))
            window.blit(fps_text, (10, 10))
            pygame.display.update()

    pygame.quit()
    quit()



if __name__ == "__main__":
    main(window)
