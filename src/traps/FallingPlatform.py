import math
import random
import pygame
from object import Object
from player import Player
from sprites import load_sprite_sheets

width = 32
height = 10
hitbox = 4


particelheigt = 100

class FallingPlatform(Object):
    ANIMATION_DELAY = 3
    PUSH_FORCE = 3  # Force applied to the player
    particles = []
    
    def __init__(self, x, y, direction="right", rotation=0):
        super().__init__(x, y, width, height, "fan")
    
        self.fire = load_sprite_sheets("Traps", "Falling Platforms", width, height)
        self.direction = direction  # can be "right", "left", "up", "down"
        self.rotation = rotation
        self.image = self.fire["Off"][0]
        self.mask = pygame.mask.Mask((width,height),True)
        self.animation_count = 0
        self.animation_name = "On"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


    def collide(self, player: Player):
        if pygame.sprite.collide_mask(self, player):
            self.rect.y += 4
            return True
        return False
    
    def draw(self, win, offset_x,offset_y):
        self.debug(win,offset_x,offset_y)
        x = self.rect.x - offset_x
        y = self.rect.y - offset_y + hitbox
    
        win.blit(self.image, (x,y))

        self.particel(win,x,y + height + 10)

    def particel(self,win,x,y): 
        
        for _ in range(2):
            randomx = random.uniform(width * 0.3, width * 1.7)
            self.particles.append({
            "start": [randomx, y],
            "pos": [randomx,0],
            "vel": [random.uniform(-0.1, 0.1), random.uniform(-3, -1)],
            "radius": random.randint(2, 4),
            "life": 60
            })

        # Partikel updaten und zeichnen
        for particle in self.particles[:]:
            particle["pos"][0] -= particle["vel"][0]
            particle["pos"][1] -= particle["vel"][1]
            particle["life"] = particle["pos"][1] 


            progress = min(1, particle["pos"][1] / particelheigt * 0.5)  # 0 bis 1
            progress_expo_radus = math.pow(0.3, 1- progress)
            ###  Radius schrumpft proportional zur Entfernung
            radius = particle["radius"] * (1 - progress_expo_radus)

      
            # Alpha-Wert reduziert sich ebenfalls
            progress_expo_alpha = math.pow(0.1, 1- progress)
            alpha = max(0, int(255 * (1 - progress_expo_alpha)))
            color = (255, 255, 255, alpha)

            surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (int(radius), int(radius)), int(radius))


            win.blit(surf, (x + particle["pos"][0] - radius, y +particle["pos"][1] - radius))

            ####Entferne tote Partikel
            if progress >= 0.8:
                self.particles.remove(particle)





# Funktion zur Distanzberechnung
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])