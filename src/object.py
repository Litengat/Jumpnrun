import pygame

from player import Player

WIDTH, HEIGHT = 1000, 800
gird_size = 96
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x * gird_size, HEIGHT - y * gird_size, gird_size, gird_size)
        self.image = pygame.Surface((gird_size, gird_size), pygame.SRCALPHA)
        self.width = gird_size
        self.height = gird_size
        self.name = name

    def draw(self, win, offset_x,offset_y):
        self.debug(win,offset_x,offset_y)
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

    def debug(self, win, offset_x,offset_y):
        pass

    def collide(player: Player):
        pass
    def loop(self):
        pass