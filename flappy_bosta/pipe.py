import pygame
from configurations import (
    PIPE_SIZE, PIPEX, PIPEY,
    PIPE_COLOR, PIPER, PIPEG, PIPEB,
    PIPE_GAP,
    PIPE_SPEED,
    PIPE_DELAY
)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, coordinates):
        super(Pipe, self).__init__()
        self.surf = pygame.Surface(PIPE_SIZE)
        self.rect = self.surf.get_rect(topleft = coordinates)
        self.mask = pygame.mask.from_surface(self.surf)
        self.surf.fill(PIPE_COLOR)
    
    def update(self):
        self.rect.move_ip((-PIPE_SPEED, 0))
        
        if self.rect.right < 0:
            self.kill()

def create_pipe(y : int):
    pipe1 = Pipe((PIPE_DELAY, y))
    pipe2 = Pipe((PIPE_DELAY, (y-PIPE_GAP)-PIPEY))
    return (pipe1, pipe2)