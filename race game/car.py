import pygame
import math
from configurations import CAR_TURN_SPEED, CAR_ACCELERATION, CAR_POWER

CAR_SPRITE = pygame.image.load(r"assets\car.png")

class Car(pygame.sprite.Sprite):
    def __init__(self, size : int, position, color, controll_keys : list):
        super(Car, self).__init__()

        self.size = size
        self.color = color
        self.radius = size//2

        # Load sprite with transparency
        self.image = CAR_SPRITE.copy()
        self.image = self._apply_team_color(self.image, self.color)

        self.surf = self.image.copy()
        
        self.rect = self.surf.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.surf)

        self.x = float(position[0])  # Floating-point trajectory position
        self.y = float(position[1])

        self.angle = 0
        self.speed = 0
        self.vx = 0  # Cached velocity components
        self.vy = 0

        self.right = controll_keys[0]
        self.forward = controll_keys[1]
        self.backward = controll_keys[2]
        self.left = controll_keys[3]
    
       def update(self, pressed_keys, friction, delta):
        if len(pressed_keys) == 0:
            control = False
        else:
            control = True
        
        if control and pressed_keys[self.right] and round(self.speed, 0) != 0:
            self.angle -= CAR_TURN_SPEED*delta
            friction *= 1.125
        elif control and pressed_keys[self.left] and round(self.speed, 0) != 0:
            self.angle += CAR_TURN_SPEED*delta
            friction *= 1.125

        max_speed = CAR_POWER/friction if self.speed > 0 else (CAR_POWER/2)/friction
        
        if control and pressed_keys[self.backward] and self.speed > -max_speed:
            self.speed -= CAR_ACCELERATION*delta
        elif control and pressed_keys[self.forward] and self.speed < max_speed:
            self.speed += CAR_ACCELERATION*delta
        elif self.speed != 0:
            if self.speed > 0:
                self.speed -= friction*delta
            elif self.speed < 0:
                self.speed += friction*delta
            if round(self.speed, 0) == 0:
                self.speed = 0

        self.vx = self.speed * math.cos(math.radians(self.angle))
        self.vy = self.speed * math.sin(math.radians(self.angle))

        self.surf = pygame.transform.rotate(self.image, -self.angle)
        
        self.rect = self.surf.get_rect(center=(int(self.x), int(self.y)))
        self.mask = pygame.mask.from_surface(self.surf)

        # Move along trajectory using floating-point precision
        self.x += self.vx*delta
        self.y += self.vy*delta
        
        # Update rect to integer position for rendering
        self.rect.center = (int(self.x), int(self.y))

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def _apply_team_color(self, sprite : pygame.surface.Surface, color) -> pygame.sprite.Sprite:
        tinted_image = sprite.copy()
        tinted_image.fill(color, special_flags=pygame.BLEND_MULT)
        return tinted_image


