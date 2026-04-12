import pygame
from configurations import (
    PLAYER_SIZE, PX, PY,
    PLAYER_COLOR, PR, PG, PB,
    FLAP_HEIGHT,
    SCY
)

class Bird(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Bird, self).__init__()
        self.surf = pygame.Surface(PLAYER_SIZE)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = pos)
        pygame.draw.circle(self.surf, PLAYER_COLOR, (PX//2, PY//2), PX//2)
        self.mask = pygame.mask.from_surface(self.surf)
        self.surf.set_colorkey((0,0,0))
        self.speed = 0
    
    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            self.rect.move_ip((0, -FLAP_HEIGHT))
            self.speed = 0
        else:
            self.speed += 0.25
            self.rect.move_ip((0, self.speed))
        
        if self.rect.bottom > SCY:
            self.rect.bottom = SCY
        elif self.rect.top < 0:
            self.rect.top = 0
            