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
    vel_y: int
    vel_x: int
    width: int
    height: int
    rect: pygame.Rect

    def __init__(this, x, y, width, height, color):
        this.rect = pygame.Rect(x, y, width, height)
        this.vel_x = 0
        this.vel_y = 0
        this.color = color

    def render(this, screen: pygame.Surface):
        pygame.draw.rect(screen, this.color, this.rect)

    def update():
        pass