import pygame
from button import *

class Menu(pygame.surface.Surface):
    def __init__(
            self, size, position, alpha,
            
            number_of_buttons, button_type, button_sizes : list, 
            buttons_colors : list, buttons_texts : list, buttons_text_colors : list, 
            buttons_font, number_of_collums, 
            
            title_text, title_font, title_color
        ):
        
        super().__init__(size, pygame.SRCALPHA)

        self.position = position
        self.alpha = alpha

        self.number_of_buttons = number_of_buttons
        self.button_type = button_type
        self.button_sizes = button_sizes
        self.buttons_colors = buttons_colors
        self.buttons_texts = buttons_texts
        self.buttons_font = buttons_font
        self.number_of_collums = number_of_collums
        self.buttons_text_colors = buttons_text_colors
        
        self.title_text = title_text
        self.title_font = title_font
        self.title_color = title_color

        self.rendered_title = self.title_font.render(self.title_text, False, self.title_color)
        self.rendered_title_rect = self.rendered_title.get_rect(center=(self.get_width()//2, self.get_height()//6))

        self.buttons = []

        self._create_buttons()

    def _create_buttons(self):
        if self.number_of_buttons % self.number_of_collums != 0:
            extra_buttons = self.number_of_buttons % self.number_of_collums
            sum_of_y_values = 0
            for i in range(self.number_of_buttons):
                sum_of_y_values += self.button_sizes[i][1]
        else:
            extra_buttons = 0
        for i in range(self.number_of_buttons):
            number_of_rows = self.number_of_buttons//self.number_of_collums

            if i >= self.number_of_buttons-extra_buttons:
                row = number_of_rows+1
                col = i-self.number_of_buttons+extra_buttons

                position = (self.get_width()//2 - self.button_sizes[i][0]*(extra_buttons-1)) + (2*col) * self.button_sizes[i][0], (self.get_height()//3 + self.button_sizes[i][1]) + row*int(3/2*(sum_of_y_values//self.number_of_buttons))
            else:
                row = i%number_of_rows
                col = i//number_of_rows

                position = (self.get_width()//2 - self.button_sizes[i][0]*(self.number_of_collums-1)) + (2*col) * self.button_sizes[i][0], (self.get_height()//3 + self.button_sizes[i][1]) + row * int(3/2*self.button_sizes[i][1])
            
            button = self.button_type(self.button_sizes[i], position, self.buttons_colors[i], self.buttons_texts[i], self.buttons_font, self.buttons_text_colors[i])
            self.buttons.append(button)
    
    def _draw_buttons(self):
        for button in self.buttons:
            button.draw(self)
    
    def _update_buttons(self, mouse_pos) -> list[bool]:
        clicked_buttons = []
        for button in self.buttons:
            clicked_buttons.append(button.update(mouse_pos))
        return clicked_buttons
    
    def draw(self, surface):
        self.fill((0, 0, 0, self.alpha))
        
        self.blit(self.rendered_title, self.rendered_title_rect)

        self._draw_buttons()
        
        surface.blit(self, self.position)
    
    def update(self, mouse_pos) -> list[bool]:
        return self._update_buttons(mouse_pos)


