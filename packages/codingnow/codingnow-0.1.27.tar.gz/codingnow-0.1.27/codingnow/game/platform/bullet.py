import pygame
from pygame import *
import pygame.time

from codingnow.game.platform.player import *

class Bullet(pygame.sprite.Sprite):
	
    def __init__(self,screen:Surface,img,player:Player):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.direction = player.direction*2
        # img = pygame.image.load(f'{filename}').convert_alpha()
        self.image_src = pygame.transform.scale(img,(40,30))
        self.image = self.image_src
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
		 

    def update(self):
        self.rect.x += self.direction            
        if self.rect.x < 0 or self.rect.right > self.screen.get_width():
            self.kill()