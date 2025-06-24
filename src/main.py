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
    """Draw the death screen with retry options"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(10)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))
    
    # Fonts for text
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    instruction_font = pygame.font.SysFont("Arial", 36)
    
    # Game Over text
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    window.blit(game_over_text, game_over_rect)
    
    # Retry instructions
    retry_text = instruction_font.render("Press R to Retry", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(retry_text, retry_rect)
    
    # Quit instructions
    quit_text = instruction_font.render("Press Q to Quit", True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    window.blit(quit_text, quit_rect)
    
    pygame.display.update()

def reset_game():
    """Reset the game to initial state"""
    player = Player(100, 100, 50, 50)
    player.DEATH = False
    objects = load_level("level")
    offset_x = 0
    offset_y = 0
    return player, objects, offset_x, offset_y

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    
    # Create a directory for levels if it doesn't exist
    os.makedirs("levels", exist_ok=True)
    
    # Load level objects from JSON
    objects = load_level("level")

    # Create floor blocks as a fallback if no level is loaded
    # floor = [Block(i * block_size, HEIGHT - block_size, block_size)
    #          for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    
    # Use level objects if available, otherwise use default level
    # if level_objects:
    #     objects = level_objects
    # else:
    #     objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
    #               Block(block_size * 3, HEIGHT - block_size * 4, block_size)]
    

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
                if player.DEATH:
                    # Handle death screen inputs
                    if event.key == pygame.K_r:
                        # Retry the level
                        player, objects, offset_x, offset_y = reset_game()
                    elif event.key == pygame.K_q:
                        # Quit the game
                        run = False
                        break
                else:
                    # Normal game inputs
                    if event.key == pygame.K_SPACE and player.jump_count < 2:
                        player.jump()
        if( player.rect.y >= 1000):
            player.death()


        # If player is dead, show death screen
        if player.DEATH:
            draw_death_screen(window)
            continue
        print(player.rect.y)

    
        for obj in objects:
            obj.loop()
        player.loop(FPS,dt)

        # fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x,offset_y)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel


        if ((player.rect.top - offset_y >= HEIGHT - scroll_area_width) and player.y_vel > 0) or (
                (player.rect.bottom - offset_y <= scroll_area_width) and player.y_vel < 0):
            offset_y += player.y_vel


        ## Fps
        font = pygame.font.SysFont("Verdana", 20)
        fps_text = font.render(str(round(clock.get_fps(), 2)), True, (255, 255, 255))
        window.blit(fps_text, (10, 10))
        pygame.display.update()
    pygame.quit()
    quit()



if __name__ == "__main__":
    main(window)
