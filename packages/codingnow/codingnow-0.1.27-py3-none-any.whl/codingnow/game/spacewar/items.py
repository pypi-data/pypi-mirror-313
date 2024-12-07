import pygame
from pygame.locals import *
from pygame import Surface
import pygame.sprite
from codingnow.game.spacewar.weapon import *
from codingnow.game.spacewar.player import *
import random
class Items(pygame.sprite.Sprite):
	def __init__(self,screen:Surface,
						img,
						cx,
						cy,
						#   weapon_img = None,
						hp=None, 
						weapon_filename = None,
						weapon_img = None,
						weapon_damage= 0,
						weapon_delay = 300,
						weapon_speed = 1,
						speed = 1
			  ):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.image = img
		self.image_src = img
		self.rect = img.get_rect()
		self.rect.centerx = cx
		self.rect.centery = cy
		self.speed = speed
		self.hp = hp
		self.weapon_filename = weapon_filename
		self.weapon_img = weapon_img
		self.weapon_damage = weapon_damage
		self.weapon_delay = weapon_delay
		self.weapon_speed = weapon_speed
		self.update_tick = 0
			
	def draw_shield(self):
		size = self.rect.width
		if size < self.rect.height:
			size = self.rect.height
		temp_surface = pygame.Surface((size,size))
		# temp_surface = pygame.Surface(self.image.get_size())
		# temp_surface.fill((0, 255, 255))
		# temp_surface.fill((0, 0, 0))
		# temp_surface.blit(self.image, (0, 0))
		cx = size/2
		cy = size/2
		pygame.draw.circle(temp_surface,(0, 255, 255),(cx,cy), self.rect.width/2)
		temp_surface.set_alpha(80)
		self.screen.blit(temp_surface, self.rect)
															
	def update(self):
		self.rect.x += self.speed
		self.draw_shield()
		if pygame.time.get_ticks() > self.update_tick:
			self.update_tick = pygame.time.get_ticks() + 200
			self.image = pygame.transform.rotate(self.image_src, random.randint(0,360))
		if self.rect.right > self.screen.get_width():
			self.kill()