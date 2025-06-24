from os.path import join
import pygame

from object import Object
from player import Player

block_size = 96


images = {
    "grass": join("assets", "Terrain", "grass.png")
}




class Block(Object):
    def __init__(self, x, y,type):
        super().__init__(x, y,block_size,block_size)
        block = get_block(type)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def collide(this, player: Player):
        return pygame.sprite.collide_mask(player,this)





def get_block(type):
    path = images[type]
    image = pygame.image.load(path).convert_alpha()

    return pygame.transform.scale(image,(96,96))


