import pygame
from object import Object
from player import Player
from sprites import load_sprite_sheets

width = 24
height = 8


class Fan(Object):
    ANIMATION_DELAY = 3
    PUSH_FORCE = 3  # Force applied to the player
    

    def __init__(self, x, y, direction="right"):
        super().__init__(x, y, width, height, "fan")
        self.fire = load_sprite_sheets("Traps", "Fan", width, height)
        self.direction = direction  # can be "right", "left", "up", "down"
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


    def collide(self, player: Player):
        if pygame.sprite.collide_mask(self, player) and self.animation_name == "On":
            if self.direction == "right":
                player.x_vel = self.PUSH_FORCE
            elif self.direction == "left":
                player.x_vel = -self.PUSH_FORCE
            elif self.direction == "up":
                player.y_vel = -self.PUSH_FORCE
            elif self.direction == "down":
                player.y_vel = self.PUSH_FORCE
            return True
        return False





