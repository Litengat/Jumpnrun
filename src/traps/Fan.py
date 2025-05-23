import random
import pygame
from object import Object
from player import Player
from sprites import load_sprite_sheets

width = 24
height = 8
hitbox = 300    

class Fan(Object):
    ANIMATION_DELAY = 3
    PUSH_FORCE = 3  # Force applied to the player
    particles = []
    

    def __init__(self, x, y, direction="right"):
        super().__init__(x, y, width, height, "fan")
        self.fire = load_sprite_sheets("Traps", "Fan", width, height)
        self.direction = direction  # can be "right", "left", "up", "down"
        self.image = self.fire["Off"][0]
        self.mask = pygame.mask.Mask((width,height + hitbox),True)
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
        # self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


    def collide(self, player: Player):
        if pygame.sprite.collide_mask(self, player) and self.animation_name == "On":
            player.jump()
        return False
    
    def draw(self, win, offset_x,offset_y):
        x = self.rect.x - offset_x
        y = self.rect.y - offset_y + hitbox
        win.blit(self.image, (x,y))
        self.particel(win,x,y)

    def particel(self,win,x,y): 
        for _ in range(5):
            self.particles.append({
            "pos": [0,0],
            "vel": [random.uniform(-1, 1), random.uniform(-3, -1)],
            "radius": random.randint(2, 5),
            "life": 60
            })

        # Partikel updaten und zeichnen
        for particle in self.particles[:]:
            particle["pos"][0] += particle["vel"][0]
            particle["pos"][1] += particle["vel"][1]
            particle["life"] = height  * 2 - particle["pos"][1] 
            # print(particle["life"])
            particle["radius"] = max(0, particle["radius"] - 0.05)

            # Transparenz (optional)
            alpha = max(0, min(255, int(particle["life"] * 4.25)))
            color = (255, 255, 255, alpha)

            surf = pygame.Surface((particle["radius"]*2, particle["radius"]*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (int(particle["radius"]), int(particle["radius"])), int(particle["radius"]))
            win.blit(surf, (x + particle["pos"][0] - particle["radius"], y +particle["pos"][1] - particle["radius"]))

            # Entferne tote Partikel
            if particle["life"] <= 0:
                self.particles.remove(particle)






