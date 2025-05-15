import pygame
from object import Object
from player import Player
from sprites import load_sprite_sheets

width = 24
height = 8


class Fan(Object):
    ANIMATION_DELAY = 3
    

    def __init__(self, x, y):
        super().__init__(x, y, width, height, "fan")
        self.fire = load_sprite_sheets("Traps", "Fan", width, height)
        print(self.fire)
        # self.angel = angel
        self.image = self.fire["Off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "Off"

    def on(self):
        self.animation_name = "On"

    def off(self):
        self.animation_name = "Off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


    # def collide(self,player: Player):
    #     if pygame.sprite.collide_mask(player,self.mask):



        
