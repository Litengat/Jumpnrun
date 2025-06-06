import math
import random
import pygame
from object import Object
from player import Player
from sprites import load_sprite_sheets

width = 38
height = 38    

class Saw(Object):
    ANIMATION_DELAY = 2
    

    def __init__(self, x, y,):
        super().__init__(x, y, width, height, "fan")
        self.saw = load_sprite_sheets("Traps", "Saw", width, height)
        self.image = self.saw["off"][0]
        self.mask = pygame.mask.Mask((width,height),True)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.saw[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        # self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


    def collide(self, player: Player):
        if pygame.sprite.collide_mask(self, player):
            player.death()
        return False
    
    def draw(self, win, offset_x,offset_y):
        x = self.rect.x - offset_x
        y = self.rect.y - offset_y
    
        win.blit(self.image, (x,y))
