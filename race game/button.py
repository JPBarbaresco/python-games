import pygame

class Button(pygame.surface.Surface):
    def __init__(self, size, position, color, text, font, text_color):
        super().__init__(size)

        self.rect = self.get_rect(center=position)

        self.original_color = color

        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color

        self.got_clicked = False

        self.set_colorkey((0,0,0))

    def draw(self, surface):
        self.fill(self.color)
        text_surf = self.font.render(self.text, False, self.text_color)
        text_rect = text_surf.get_rect(center=(self.get_width()//2, self.get_height()//2))
        self.blit(text_surf, text_rect)

        surface.blit(self, self.rect)
    
    def is_clicked(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]
    
    def is_released(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos) and not pygame.mouse.get_pressed()[0]
    
    def update(self, mouse_pos) -> bool:
        if self.is_clicked(mouse_pos) and not self.got_clicked:
            self.color = (max((self.color[0]-50, 0)), max((self.color[1]-50, 0)), max((self.color[2]-50, 0)))
            self.got_clicked = True
            return False
        elif self.is_released(mouse_pos) and self.got_clicked:
            self.color = self.original_color
            self.got_clicked = False
            return True
        elif not self.got_clicked:
            self.color = self.original_color
            self.got_clicked = False
            return False