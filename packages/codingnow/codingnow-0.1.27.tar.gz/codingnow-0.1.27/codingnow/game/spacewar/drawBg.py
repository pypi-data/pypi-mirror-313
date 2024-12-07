import pygame
from pygame.locals import *
from pygame import Surface

class DrawBg():
	def __init__(self,screen:Surface):
		self.screen = screen
		# self.filename = filename
		# img = pygame.image.load(f'{filename}')
		# self.image = pygame.transform.scale(img, (rect.width, rect.height))
		# self.rect = self.image.get_rect()
		self.rect = pygame.Rect(0,0,self.screen.get_width(), self.screen.get_height())
		self.rect2 = self.rect.copy()
		self.width = self.rect.width

	def draw(self, image):
		# pygame.draw.rect(self.screen,(255,255,255),rect,1)  
		
		self.rect.x += 1
		if self.rect.x >= self.width:
			self.rect.x = 0
		self.rect2.right = self.rect.left
		
		self.screen.blit(image,self.rect2)
		self.screen.blit(image,self.rect)