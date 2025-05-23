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
    if x > WIDTH or y > HEIGHT or x < 0 or y < 0:
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
            player.make_hit()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    
    # Create a directory for levels if it doesn't exist
    os.makedirs("levels", exist_ok=True)
    
    # Load level objects from JSON
    objects = load_level("level")
    fan = Fan(100,100,"up")

    objects.append(fan)
    
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
    fan.on()
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
        fan.loop()
        player.loop(FPS)
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
