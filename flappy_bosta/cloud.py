import pygame
import random
from configurations import (
    CLOUD_MAXX, CLOUD_MAXY, CLOUD_MINX, CLOUD_MINY,
    CLOUD_MAX_ALPHA, CLOUD_MIN_ALPHA,
)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super(Cloud, self).__init__()
        self.surf = pygame.Surface((random.randint(CLOUD_MINX, CLOUD_MAXX), random.randint(CLOUD_MINY, CLOUD_MAXY)))
        self.rect = self.surf.get_rect(topleft = coordinates)
        self.surf.fill((255,255,255))
        self.surf.set_alpha(random.randint(CLOUD_MIN_ALPHA, CLOUD_MAX_ALPHA))
        
    def update(self):
        self.rect.move_ip((-1, 0))

        if self.rect.right < 0:
            self.kill()

def create_cloud(xy):
    cloud = Cloud(xy)
    return cloud