import pygame

from player import Player

WIDTH, HEIGHT = 1000, 800
gird_size = 96
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x * gird_size, HEIGHT - y * gird_size, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x,offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
    
    def collide(player: Player):
        pass