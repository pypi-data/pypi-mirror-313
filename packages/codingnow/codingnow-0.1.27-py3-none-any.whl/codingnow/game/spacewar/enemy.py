import pygame
from pygame.locals import *
from pygame import Surface
import pygame.sprite
from codingnow.game.spacewar.weapon import *
from codingnow.game.spacewar.player import *

class Enemy(pygame.sprite.Sprite):
	group_weapon = pygame.sprite.Group()
	def __init__(self,screen:Surface,player, img,
											hp = 100, 
											speed = 1,
											w_img=None, 
											w_damage = 10, 
											w_speed = 1, 
											w_delay = 1000,
											
											i_img=None,
											i_hp=0,
											i_weapon_filename = None,
											i_weapon_img = None,
											i_weapon_damage=0,
											i_weapon_delay=0,
											i_weapon_speed=0,
											
											):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.hp_max = hp
		self.hp = hp
		self.speed = speed
		
		self.player = player
			
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		self.prog_width = int(self.rect.width*0.7)
		self.prog_height = int(self.rect.height*0.3)
		if self.prog_width > 50:
			self.prog_width = 50
			
		if self.prog_width < 20:
			self.prog_width = 20
			
		if self.prog_height > 20:
			self.prog_height = 20
		if self.prog_height < 5:
			self.prog_height = 5
			
		self.rect_hp = pygame.Rect(0,0,self.prog_width,self.prog_height)
		
		self.w_image = w_img
		self.w_damage = w_damage
		self.w_speed = w_speed
		self.w_delay = w_delay
		self.weapon_tick = pygame.time.get_ticks()+self.w_delay
		
		self.i_img = i_img
		self.i_hp = i_hp
		self.i_weapon_filename = i_weapon_filename
		self.i_weapon_img = i_weapon_img
		self.i_weapon_damage = i_weapon_damage
		self.i_weapon_delay = i_weapon_delay
		self.i_weapon_speed = i_weapon_speed
		
		self.shield_tick = 0
		self.shield_on = False
		
	def draw_weapon(self):
		if self.w_image is not None:
			if self.weapon_tick < pygame.time.get_ticks():
				self.weapon_tick = pygame.time.get_ticks()+self.w_delay
				cx = self.rect.centerx
				cy = self.rect.centery
				target_y = None
				if self.player is not None:
					target_y = self.player.rect.y
				weapon = Weapon(self.screen,self.w_image,cx,cy,self.w_damage,self.w_speed,target_y)
				self.group_weapon.add(weapon)						
		
				
	def draw_shield(self):		
		if self.shield_on:
			self.shield_tick = pygame.time.get_ticks()
			self.shield_on = False
			
		if self.shield_tick > 0:
			ellip = pygame.time.get_ticks() - self.shield_tick
			if ellip < 500:
				temp_surface = pygame.Surface(self.image.get_size())
				temp_surface.fill((255, 0, 255))
				temp_surface.blit(self.image, (0, 0))
				temp_surface.set_alpha(80)
				self.screen.blit(temp_surface, self.rect)
			else:
				self.shield_tick = 0
				
	def draw_hp(self):		
		self.rect_hp.x = self.rect.x
		self.rect_hp.bottom = self.rect.top
		
		temp_surface = pygame.Surface((self.rect_hp.width,self.rect_hp.height))
		temp_surface.fill((0, 0, 0))
		rect = self.rect_hp.copy()
		rect.x = 0
		rect.y = 0
		pygame.draw.rect(temp_surface,(255,255,255),rect,1)
		
		prog = self.prog_width * self.hp/self.hp_max
		rect.width = prog
		pygame.draw.rect(temp_surface,(255,0,0),rect,0)  
		
		# temp_surface.blit(self.image, (0, 0))
		temp_surface.set_alpha(100)
		self.screen.blit(temp_surface, self.rect_hp)
				
	def update(self):
		self.rect.x += self.speed
		self.draw_shield()
		self.draw_weapon()
		self.draw_hp()
		self.group_weapon.update()
		self.group_weapon.draw(self.screen)
		
		if self.rect.right > self.screen.get_width():
			self.kill()