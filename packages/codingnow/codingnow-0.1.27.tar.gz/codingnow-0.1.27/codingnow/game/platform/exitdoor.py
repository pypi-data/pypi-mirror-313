import pygame
from pygame import Surface
import pygame.sprite
import pygame.transform

class ExitDoor(pygame.sprite.Sprite):
    def __init__(self,screen:Surface, img,x:int, y:int):
        pygame.sprite.Sprite.__init__(self)
                    
        self.screen = screen        
        # img = pygame.image.load(f'{filename}').convert_alpha()
        self.image_src = pygame.transform.scale(img,(60,60))
        self.image = self.image_src
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
    def update(self):
        pass