from geometry.vector import Vector
from geometry.rectangle import Rectangle

import pygame

class Button:
    def __init__(self, text, x, y, hw, hh, on_click, font, font_col):
        self.text = text
        # the shape the button will be
        self.rect = Rectangle(x, y, hw, hh)
        # a function that is called when the button is clicked
        self.on_click = on_click
        # the text that will be displayed
        self.text_render = font.render(self.text, False, font_col)
        # wether the button is currently being pressed or not
        self.pressed = False

    def draw(self, screen):
        # draw the button's rectangle
        pygame.draw.rect(screen, (126, 126, 126), self.rect.corner_rect_tuple())
        # draw the button's text
        screen.blit(self.text_render, Vector.to_tuple(self.rect.top_left_pos()))

    def check_mouse_down(self, mouse_pos):
        # if the mouse is pressed, and it is in the button's rectangle, update the pressed variable
        if self.rect.contains_point(mouse_pos):
            self.pressed = True
        
    def check_mouse_up(self, mouse_pos):
        # if the mouse is released and the button was pressed before and the mouse is in the button's rectangle, call the given on_click function
        if self.pressed and self.rect.contains_point(mouse_pos):
            # the button should never be pressed right after the mouse is released
            self.pressed = False
            print(self.text)
            return self.on_click()
    