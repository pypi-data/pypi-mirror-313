import pygame
from pygame.locals import *
from pygame import Surface
from codingnow.game.spacewar.player import *

class DrawMsg():
	msg_score_text = None
	msg_level_text = None
	msg_weapon_text = None
	msg_hp_text = None
	msg_status = None
	msg_status_list = []
	msg_status_tick = 0
	
	def __init__(self,screen:Surface):
		self.screen = screen
		self.mfont = pygame.font.SysFont('malgungothic', 20)
		self.mfontGV = pygame.font.SysFont('malgungothic', 100)
		self.mfontRE = pygame.font.SysFont('malgungothic', 50)
                
	def set_msg_score(self, x=10,y=10, color = (0,0,0), text = '점수 : '):
		self.msg_score_x = x
		self.msg_score_y = y
		self.msg_score_color = color
		self.msg_score_text = text
		
	def set_msg_level(self, x=10,y=50, color = (0,0,0), text = '레벨 : '):
		self.msg_level_x = x
		self.msg_level_y = y
		self.msg_level_color = color
		self.msg_level_text = text
		
	def set_msg_weapon(self, x=10,y=90, color = (0,0,0), text = '무기 : '):
		self.msg_weapon_x = x
		self.msg_weapon_y = y
		self.msg_weapon_color = color
		self.msg_weapon_text = text
		
	def set_msg_hp(self, x=10,y=130, color = (0,0,0), text = 'HP : '):
		self.msg_hp_x = x
		self.msg_hp_y = y
		self.msg_hp_color = color
		self.msg_hp_text = text
		
	def draw_message(self, msg:str, color:tuple, x:int, y:int):
		msg = f'{msg}'
		img = self.mfont.render(msg, True, color,(0,0,0))
		img.set_alpha(100)
		self.screen.blit(img, (x, y))
		
	def draw_gameOver(self,player:Player):
		if (player is not None) and player.game_over:
			msg = f'Game Over!!'
			img = self.mfontGV.render(msg, True, (192,0,0))
			img.set_alpha(100)
			rect = img.get_rect()
			rect.centerx = self.screen.get_width()/2
			rect.centery = self.screen.get_height()/2-100
			self.screen.blit(img, rect)
			
			msg = f'재시작 (클릭)'
			img = self.mfontRE.render(msg, True, (192,0,192))
			rect = img.get_rect()
			rect.centerx = self.screen.get_width()/2
			rect.centery = self.screen.get_height()/2
			self.screen.blit(img, rect)
			mouse_pos = pygame.mouse.get_pos()
			if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
				return True
		return False
	
	def set_status_msg(self, msg):
		self.msg_status_list.append(msg)
		
	def draw_status_msg(self):
		if len(self.msg_status_list):
			if self.msg_status_tick == 0:
				self.msg_status = self.msg_status_list.pop()
				self.msg_status_tick = pygame.time.get_ticks()+1000
				
		if self.msg_status_tick < pygame.time.get_ticks():
			self.msg_status_tick = 0
			self.msg_status = None
				
		if self.msg_status is not None:
			img = self.mfontGV.render(self.msg_status, True, (192,0,0))
			img.set_alpha(100)
			rect = img.get_rect()
			rect.centerx = self.screen.get_width()/2
			rect.centery = self.screen.get_height()/2-100
			self.screen.blit(img, rect)
			
	def draw(self,player:Player):		
		if (self.msg_score_text is not None) and (player is not None):
			self.draw_message(f'{self.msg_score_text}{player.score}',
							self.msg_score_color, 
							x=self.msg_score_x,
							y=self.msg_score_y)

		if self.msg_level_text is not None and (player is not None):
			self.draw_message(f'{self.msg_level_text}{player.level}',
							self.msg_level_color, 
							x=self.msg_level_x,
							y=self.msg_level_y)
			
		if self.msg_weapon_text is not None and (player is not None):
			self.draw_message(f'{self.msg_weapon_text}{player.weapon_damage}',
							self.msg_weapon_color, 
							x=self.msg_weapon_x,
							y=self.msg_weapon_y)
			
		if (self.msg_hp_text is not None) and (player is not None):
			self.draw_message(f'{self.msg_hp_text}{player.hp}',
							self.msg_hp_color, 
							x=self.msg_hp_x,
							y=self.msg_hp_y)
		self.draw_status_msg()
		return self.draw_gameOver(player)