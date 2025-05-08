


import pygame
from object import Object

WIDTH, HEIGHT = 800, 600

player_width = 50
player_height = 60
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0

class Player(Object):
    x: int
    y: int
    width: int
    height: int
    rect: pygame.Rect

    def __init__(this):
        this.rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
    def render(this,screen: pygame.Surface):
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 0, 100, 100))


    def update():
        pass