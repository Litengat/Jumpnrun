import pygame
import os
from os.path import join
from object import Object
from sprites import load_sprite_sheets

width = 64
height = 64 


class Finish(Object):
    ANIMATION_DELAY = 3
    
    def __init__(self, x, y):
        super().__init__(x, y, width, height)
        self.name = "finish"
        self.animation_count = 0
        self.animation_name = "Idle"
        
        # Load sprites
        self.sprites = load_sprite_sheets("Checkpoints", "End", width, height)
        self.image = self.sprites["Idle"][0]
        
    
    def loop(self):
        sprites = self.sprites[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    
    def activate(self):
        """Activate the finish line"""
        if not self.activated:
            self.activated = True
            return True  # Return True when first activated
        return False
    
    def collide(self, player):
        if pygame.sprite.collide_mask(self, player):
            self.animation_name = "Pressed"
            print("Finish line reached!")
            player.WINNING = True

            return True
        return False
