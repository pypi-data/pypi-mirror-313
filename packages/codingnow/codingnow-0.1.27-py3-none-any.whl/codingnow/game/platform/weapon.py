import pygame
from pygame import Surface
import pygame.sprite
import pygame.transform
import random

class Weapon(pygame.sprite.Sprite):
    def __init__(self,screen:Surface, filename,img,x:int, y:int):
        pygame.sprite.Sprite.__init__(self)
        self.filename = filename
        self.screen = screen        
        # img = pygame.image.load(f'{filename}').convert_alpha()
        self.image_src = pygame.transform.scale(img,(30,30))
        self.image = self.image_src
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay_counter = 0
        self.angle = 0
        
        
    def update(self):
        self.delay_counter += 1
        if abs(self.delay_counter) > 5:
            self.delay_counter = 0
            self.angle = random.randint(0,360)
            self.image = pygame.transform.rotate(self.image_src, self.angle)