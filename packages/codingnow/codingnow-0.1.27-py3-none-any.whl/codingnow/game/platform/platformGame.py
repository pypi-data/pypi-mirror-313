
import os
try:
    import pygame
except:
    os.system('pip install pygame')
    import pygame
    
import pygame.draw
import pygame.mouse
import pygame.rect
import pygame.sprite
from pygame.event import Event

try:
    import clipboard
except:
    os.system('pip install clipboard')
    import clipboard

from codingnow.game.platform.player import *
from codingnow.game.platform.block import *
from codingnow.game.platform.coin import *
from codingnow.game.platform.monster import *
from codingnow.game.platform.lava import *
from codingnow.game.platform.bullet import *
from codingnow.game.platform.exitdoor import *
from codingnow.game.platform.weapon import *
from codingnow.game.platform.hp import *

class PlatformGame():
    player:Player = None
    on_mouse_point = False
    event_func_p = None
    bgimgs = {}
    image_sto = {}
    lastExt = 0
    def __init__(self,screen:Surface) -> None:
        self.screen = screen
        self.player = None
        self.group_block = pygame.sprite.Group()
        self.group_coin = pygame.sprite.Group()
        self.group_lava = pygame.sprite.Group()
        self.group_monster = pygame.sprite.Group()
        self.group_exitDoor = pygame.sprite.Group()
        self.group_weapon = pygame.sprite.Group()
        self.group_bullet = pygame.sprite.Group()
        self.group_hp = pygame.sprite.Group()
        self.image_bg = None
        self.map_data = {}
        self.msg_status=[]
        self.msg_status_curr = ''
        self.msg_status_tick = 0
        self.copy_pressed = False
        # self.event_func_p = self.event_func()
        self.mfont30 = pygame.font.SysFont('malgungothic', 30)    

    def map_change(self, level):
        self.group_bullet.empty()
        self.group_coin.empty()
        self.group_monster.empty()
        self.group_block.empty()
        self.group_lava.empty()
        self.group_exitDoor.empty()
        self.group_weapon.empty()
        self.group_hp.empty()
        try:            
            if level not in self.map_data:
                level = 1
                
            if level not in self.map_data:
                return None
            for key in self.map_data[level]:
                item = self.map_data[level][key]
                
                for values in item:
                    filename = values[0]
                    
                    if filename not in self.image_sto:
                        self.image_sto[filename] = pygame.image.load(f'{filename}').convert_alpha()
                    # else:
                    #     print('aa')
                    img = self.image_sto[filename]
                    
                    x  = values[1]
                    y  = values[2]                        
                    if key == 'block':
                        move_x = values[3] 
                        move_y = values[4]
                        self.group_block.add(Block(self.screen,img,x,y,move_x,move_y))
                    if key == 'coin':
                        self.group_coin.add(Coin(self.screen,img,x,y))
                    if key == 'hp':
                        self.group_hp.add(Hp(self.screen,img,x,y))
                    if key == 'monster':
                        move_x = values[3] 
                        move_y = values[4]
                        self.group_monster.add(Monster(self.screen,img,x,y,move_x,move_y))
                    if key == 'exit':
                        self.group_exitDoor.add(ExitDoor(self.screen,img,x,y))
                    if key == 'lava':
                        self.group_lava.add(Lava(self.screen,img,x,y))
                    if key == 'weapon':
                        self.group_weapon.add(Weapon(self.screen,filename,img,x,y))
                        
        except Exception as ex:
            print(ex)
            
        return level
    
    def event_func(event:Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # print('aaaa')
                pass
                
    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.event_func_p is not None:
                self.event_func_p(event)
        return True

    def add_player(self,filename:str, flip:bool=False, width:int=60, height:int=60):
        self.player = Player(self,self.screen,filename,width,height,flip)
        return self.player
    
    def add_bg_image(self, filename:str,level:int=1):        
        img = pygame.image.load(f'{filename}').convert_alpha()
        image_bg = pygame.transform.scale(img,(self.screen.get_width(),self.screen.get_height()))
        if (level != 1) and (1 not in self.bgimgs):
            self.bgimgs[1] = image_bg
            
        self.bgimgs[level] = image_bg
        # print(self.bgimgs)

    def check_map_init(self, level, key):
        if level not in self.map_data:
            self.map_data.update({level:{}})
        if key not in self.map_data[level]:
            self.map_data[level].update({key:[]})
        
    def add_map_block(self,level:int, filename:str, x:int, y:int,move_x:int=0,move_y:int=0, num:int=1):
        self.check_map_init(level,'block')            
        # self.map_data[level]['block'].append([filename,x,y,move_x,move_y])
        for i in range(num):
            self.map_data[level]['block'].append([filename,x+60*i,y,move_x,move_y])
        
    def add_map_coin(self,level:int, filename:str, x:int, y:int):
        self.check_map_init(level,'coin')            
        self.map_data[level]['coin'].append([filename,x,y])        
                
    def add_map_hp(self,level:int, filename:str, x:int, y:int):
        self.check_map_init(level,'hp')            
        self.map_data[level]['hp'].append([filename,x,y])    
        
    def add_map_weapon(self,level:int, filename:str, x:int, y:int):
        self.check_map_init(level,'weapon')            
        self.map_data[level]['weapon'].append([filename,x,y])  
        # if self.player is not None:
        #     self.player.set_bullet_img(filename)
            
        
    def add_map_mons(self,level:int, filename:str, x:int, y:int,move_x:int=1,move_y:int=0):
        self.check_map_init(level,'monster')
        self.map_data[level]['monster'].append([filename,x,y,move_x,move_y])
        
    def add_map_lava(self,level:int, filename:str, x:int, y:int, num:int):
        self.check_map_init(level,'lava')        
        for i in range(num):
            self.map_data[level]['lava'].append([filename,x+30*i,y])
        
    def add_map_exit(self,level:int, filename:str, x:int, y:int):
        self.check_map_init(level,'exit')
        self.map_data[level]['exit'].append([filename,x,y])
        if self.lastExt < level:
            self.lastExt = level

    def add_bullet(self,filename):
        if filename not in self.image_sto:
            self.image_sto[filename] = pygame.image.load(f'{filename}').convert_alpha()
        img = self.image_sto[filename]
        self.group_bullet.add(Bullet(self.screen,img,self.player))
        
    def draw_mouse_point(self):
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            x,y = pygame.mouse.get_pos()
            x = x - (x%10)
            y = y - (y%10)
            # pygame.mouse.set_pos(x,y)
            
            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_LCTRL] and key_press[pygame.K_c] or pygame.mouse.get_pressed()[0]:
                if self.copy_pressed == False:
                    clipboard.copy(f"x={x},y={y}")
                    self.msg_status.append(f'복사 X:{x},Y:{y}')
                    self.copy_pressed = True
            else:
                self.copy_pressed = False
            
            msg = f'X:{x},Y:{y}'
            img = self.mfont30.render(msg, True, (255,255,255))
            rect = img.get_rect()
            # rect.centerx = x
            # rect.bottom = y
            rect.right = self.screen.get_width()
            rect.y = 0
            pygame.draw.line(self.screen,(192,192,192),(x,0),(x,self.screen.get_height()),1)
            pygame.draw.line(self.screen,(192,192,192),(0,y),(self.screen.get_width(),y),1)
            
            temp_surface = Surface((60,30))            
            pygame.draw.rect(temp_surface,(0,192,192),(0,0,60,30))
            temp_surface.set_alpha(100)
            self.screen.blit(temp_surface, (x,y,60,30))
            
            if rect.x < 0:
                rect.x = 0
            if rect.right > self.screen.get_width():
                rect.right = self.screen.get_width()
                
            if rect.y < 0:
                rect.y = 0
            if rect.bottom > self.screen.get_height():
                rect.bottom = self.screen.get_height()
                
            # self.screen.blit(img, rect)
            temp_surface = pygame.Surface((rect.width, rect.height))
            temp_surface.fill((0,0,0))
            temp_surface.set_alpha(100)
            temp_surface.blit(img,(0,0))
            self.screen.blit(temp_surface, rect)
            
    def draw_status_msg(self):
        if len(self.msg_status) and self.msg_status_tick == 0:
            self.msg_status_curr = self.msg_status.pop()
            self.msg_status_tick = pygame.time.get_ticks()+1000
            
        if self.msg_status_tick != 0:
            if self.msg_status_tick < pygame.time.get_ticks():
                self.msg_status_tick = 0
                self.msg_status_curr = ''
            else:
                img = self.mfont30.render(self.msg_status_curr, True, (255,255,255),(0,0,0))
                img.set_alpha(80)
                rect = img.get_rect()
                rect.centerx = self.screen.get_width()/2
                rect.centery = self.screen.get_height()/2
                self.screen.blit(img, rect)
                
    def draw_bg_img(self):
        img = None
        if self.player is not None:
            if self.player.level in self.bgimgs:
                img = self.bgimgs[self.player.level]
                
        if img is None:
            if 1 in self.bgimgs:
                img = self.bgimgs[1]
            
        if img is not None:
            self.screen.blit(img,(0,0))
            
    def draw(self):        
        self.draw_bg_img()
        
        if self.player is not None:
            self.player.draw()
            
        for bullet in self.group_bullet:
            if pygame.sprite.spritecollide(bullet, self.group_monster, True):
                bullet.kill()
                self.player.score += 20
                if self.player.snd_dic['monster'] is not None:
                    self.player.snd_dic['monster'].play()
        
        self.group_block.update()
        self.group_coin.update()
        self.group_hp.update()
        self.group_weapon.update()
        self.group_monster.update()
        self.group_lava.update()
        self.group_bullet.update()
        self.group_exitDoor.update()
        
        self.group_exitDoor.draw(self.screen)
        self.group_block.draw(self.screen)
        self.group_coin.draw(self.screen)
        self.group_hp.draw(self.screen)
        self.group_weapon.draw(self.screen)
        self.group_monster.draw(self.screen)
        self.group_lava.draw(self.screen)
        self.group_bullet.draw(self.screen)
        if self.on_mouse_point:
            self.draw_mouse_point()
            
        self.draw_status_msg()