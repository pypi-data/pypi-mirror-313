import pygame
from pygame.locals import *
from pygame import Surface
import pygame.sprite

class Weapon(pygame.sprite.Sprite):
	
	def __init__(self,screen:Surface,img,cx, cy,damage = 100, speed = 1, target_y = None):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.damage = damage
		self.speed = speed
			
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.centerx = cx
		self.rect.centery = cy
		
		self.target_y = target_y
		self.target_tick = pygame.time.get_ticks() + 300
		self.target_limit = pygame.time.get_ticks() + 400
						
	def update(self):		
		
		if self.target_y is not None:			
			if self.target_tick < pygame.time.get_ticks():
				self.rect.x += self.speed
				
				if self.target_limit > pygame.time.get_ticks():
					if self.rect.y > self.target_y:
						self.rect.y -= self.speed
					if self.rect.y < self.target_y:
						self.rect.y += self.speed
		else:
			self.rect.x += self.speed
			
		if (self.rect.right > self.screen.get_width()) or (self.rect.left < 0):
			self.kill()