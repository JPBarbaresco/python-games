import pygame

class Camera(pygame.surface.Surface):
    def __init__(self, size, position, target : pygame.sprite.Sprite):
        super().__init__(size)

        self.rect = self.get_rect(center = position)

        self.target = target

        self.set_colorkey((0,0,0))
    
    def update(self):
        self.rect.center = self.target.rect.center

        self.fill((0,0,0))