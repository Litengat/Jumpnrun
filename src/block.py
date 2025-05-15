from os.path import join
import pygame

from object import Object

block_size = 96
WIDTH, HEIGHT = 1000, 800

images = {
    "grass": join("assets", "Terrain", "grass.png")
}




class Block(Object):
    def __init__(self, x, y, size,type):
        super().__init__(x * block_size, HEIGHT - y * block_size, size, size)
        block = get_block(type)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


def get_block(type):
    path = images[type]
    image = pygame.image.load(path).convert_alpha()

    return pygame.transform.scale(image,(96,96))
