import pygame
from pygame.locals import *
from pygame import Surface

class Lava(pygame.sprite.Sprite):
	def __init__(self,screen:Surface, img,x:int, y:int):
		pygame.sprite.Sprite.__init__(self)

		self.screen = screen        
		# img = pygame.image.load(f'{filename}').convert_alpha()
		self.image_src = pygame.transform.scale(img,(30,30))
		self.image = self.image_src
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = 1
		self.delay_counter = 0

	def update(self):
		self.delay_counter += 1
		if self.delay_counter > 5:
			self.direction *= -1
			self.delay_counter *= -1
			self.rect.x += self.direction