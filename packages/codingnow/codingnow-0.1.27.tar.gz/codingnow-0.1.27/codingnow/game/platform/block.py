import pygame
from pygame import Surface
import pygame.sprite
import pygame.transform

class Block(pygame.sprite.Sprite):

    def __init__(self,screen:Surface, img, x:int, y:int,move_x:int=0,move_y:int=0):
        pygame.sprite.Sprite.__init__(self)
            
        self.screen = screen        
        # img = pygame.image.load(f'{filename}').convert_alpha()
        self.image = pygame.transform.scale(img,(60,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay_counter = 0
        self.direction = 1
        self.move_x = move_x
        self.move_y = move_y
        
        
    def update(self):
        self.rect.x += self.direction * self.move_x
        self.rect.y += self.direction * self.move_y
        self.delay_counter += 1
        if abs(self.delay_counter) > 50:
            self.direction *= -1
            self.delay_counter *= -1