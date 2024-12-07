import pygame
from pygame.locals import *
from pygame import Surface

class DrawImg():
	def __init__(self,screen:Surface,filename, rect:pygame.Rect):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.filename = filename
		img = pygame.image.load(f'{filename}')
		size_offset = 4
		self.image = pygame.transform.scale(img, (rect.width-size_offset, rect.height-size_offset))
		self.rect = self.image.get_rect()
		self.rect.x = rect.x+size_offset/2
		self.rect.y = rect.y+size_offset/2

	def draw(self,rect:pygame.Rect):
		# pygame.draw.rect(self.screen,(255,255,255),rect,1)  
		self.screen.blit(self.image,rect)