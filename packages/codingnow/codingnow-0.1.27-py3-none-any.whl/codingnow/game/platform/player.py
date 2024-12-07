import pygame
from pygame import Surface
import pygame.transform
import random


class Player():
    speed = 0
    JUMP = 15
    jumped = False
    jump_y = 0
    score = 0
    level = 1
    level_real = 1
    gameover = False
    direction = 2
    hp = 3
    weapons = []
    imgs = {}
    jump_cnt = 0
    gametime = 0
    gametime_tick = 0
    MissionCompleted = False
    
    start_position = {1:{'x' : 20,'y':510}}
    def __init__(self,parent,screen:Surface,filename:str, width:int, height:int,flip: bool) -> None:
        self.parent = parent
        self.screen = screen
        self.img_gameover = None  
        self.rect = None
        self.image = None
        self.image = self.set_img(self.level, filename,flip,width,height)
        self.img_idex = 0
        
        # self.image = self.get_img()
        # self.rect = self.image.get_rect()
        self.game_reset(True)
        self.weapon_pressed = False
        # self.image_bullet = None        
        self.msg_level_text = None
        self.msg_score_text = None
        self.msg_weapon_text = None
        self.msg_hp_text = None
        self.msg_jumpcnt_text = None
        self.msg_gametime_text = None
        self.mfont20 = pygame.font.SysFont('malgungothic', 20)
        self.mfont30 = pygame.font.SysFont('malgungothic', 30)
        self.mfont40 = pygame.font.SysFont('malgungothic', 40)
        self.mfont50 = pygame.font.SysFont('malgungothic', 50)
        self.mfont60 = pygame.font.SysFont('malgungothic', 60)
        
        # self.set_gameover_image('ghost.png')
        #효과음
        self.snd_dic = {
            'weapon':None,
            'coin':None,
            'jump':None,
            'monster':None,
            'game_over':None,
        }
        
    def get_position(self, level=1):
        if level in self.start_position:
            x = self.start_position[level]['x']
            y = self.start_position[level]['y']
        else:
            x = self.start_position[1]['x']
            y = self.start_position[1]['y']
        return x,y
            
    def set_position(self, level:int,x:int=20,y:int=510):
        self.start_position[level] = {}
        x = self.start_position[level]['x'] = x
        y = self.start_position[level]['y'] = y
            
    def get_img(self, level=1, dir='right'):
        if level in self.imgs:
            img = self.imgs[self.level][dir][self.img_idex]
        else:
            img = self.imgs[1][dir][self.img_idex]
        
        rect = img.get_rect()
        rect.x = self.rect.x
        rect.y = self.rect.y
        self.rect = rect
        return img
        
    def set_img(self, level:int, filename:str, flip:bool=False, width:int=60, height:int=60):  
        
        self.imgs[level] = {
            'left':[],
            'right':[],
            }
         
        img = pygame.image.load(f'{filename}').convert_alpha()     
        if flip:
            image_src_l = pygame.transform.scale(img,(width,height))
            image_src_r = pygame.transform.flip(image_src_l,True,False)
        else:
            image_src_r = pygame.transform.scale(img,(width,height))
            image_src_l = pygame.transform.flip(image_src_r,True,False)
        self.imgs[level]['left'].append(image_src_l)
        self.imgs[level]['right'].append(image_src_r)
        
        if self.level == level:
            self.image = image_src_r
            if self.rect is not None:
                self.get_img(level)
                # self.rect.x,self.rect.y = self.get_position(self.level)      
                self.rect_pre = self.rect.copy()
            else:
                self.rect = self.image.get_rect()
                
        return image_src_r
        
    def set_gameover_image(self,filename):
        img = pygame.image.load(f'{filename}').convert_alpha()
        self.img_gameover = pygame.transform.scale(img,(self.rect.width,self.rect.height))
        
    def game_reset(self, reload_map):
        self.score = 0
        self.level = 1      
        self.level_real = 1  
        self.weapons.clear()
        self.hp = 3
        self.jump_cnt = 0
        self.image = self.get_img(self.level)
        self.MissionCompleted = False
        self.gametime = 0
        self.gametime_tick = pygame.time.get_ticks() + 10
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = self.get_position(self.level) 
        self.rect_pre = self.rect.copy()
        
        self.gameover = False
        if reload_map:
            self.parent.map_change(self.level)
    
    # def set_bullet_img(self,filename):        
    #     img = pygame.image.load(f'{filename}').convert_alpha()
    #     self.image_bullet = pygame.transform.scale(img,(40,30))
        
    def set_snd_weapon(self,filename):
        self.snd_dic['weapon'] = pygame.mixer.Sound(filename)
        
    def set_snd_coin(self,filename):
        self.snd_dic['coin'] = pygame.mixer.Sound(filename)
        
    def set_snd_jump(self,filename):
        self.snd_dic['jump'] = pygame.mixer.Sound(filename)
        
    def set_snd_game_over(self,filename):
        self.snd_dic['game_over'] = pygame.mixer.Sound(filename)
        
    def set_snd_monster(self,filename):
        self.snd_dic['monster'] = pygame.mixer.Sound(filename)
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image_src,angle)

    def check_img_dir(self):
        if self.rect_pre.x < self.rect.x:
            self.image = self.get_img(self.level, 'right')
            self.direction = 2
        if self.rect_pre.x > self.rect.x:
            self.image = self.get_img(self.level, 'left')
            self.direction = -2
            
        
    def check_img_screen_limit(self):        
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            self.jumped = False
            
        
    def key_pressed(self):
        if self.speed == 0:
            return
        key_press = pygame.key.get_pressed()
        
        # if len(self.parent.group_block)==0:
        #     if key_press[pygame.K_UP]:
        #         self.rect.centery -= self.speed

        #     if key_press[pygame.K_DOWN]:
        #         self.rect.centery += self.speed
                
        if key_press[pygame.K_RETURN]:
            if len(self.weapons) > 0 and self.weapon_pressed==False:
                self.weapon_pressed = True
                filename = self.weapons.pop()
                self.parent.add_bullet(filename)
                if self.snd_dic['weapon'] is not None:
                    self.snd_dic['weapon'].play()
        else:
            self.weapon_pressed = False
            
            
        if key_press[pygame.K_LEFT]:
            top = self.check_up_colliderect_blocks(-self.speed)
            if top:
                self.rect.bottom = top
                self.rect_pre = self.rect.copy()
            self.rect.centerx -= self.speed
            
        if key_press[pygame.K_RIGHT]:
            top = self.check_up_colliderect_blocks(self.speed)
            if top:
                self.rect.bottom = top
                self.rect_pre = self.rect.copy()
            self.rect.centerx += self.speed
            
        if key_press[pygame.K_SPACE]:
            self.jump()
            
            
    def jump(self):
        if self.jumped == False:
            self.jump_cnt += 1
            if self.snd_dic['jump'] is not None:
                self.snd_dic['jump'].play()
            self.jump_y = self.JUMP * (-1)
            self.jumped = True
            
    def jump_process(self):
        dy = 0
        if len(self.parent.group_block)>0:
            self.jump_y += 1
            if self.jump_y > self.JUMP:
                self.jump_y = 1#self.JUMP
            dy = self.jump_y
        else:
            if self.jumped:
                if self.jump_y+1 >= self.JUMP:
                    self.jumped = False
                else:
                    self.jump_y += 1
                    dy = self.jump_y
        return dy
    
    def check_up_colliderect_blocks(self,dx):
        xc = pygame.Rect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height)#앞으로        
        top = 0
        for i,block in enumerate(self.parent.group_block):
            brect = block.rect.copy()
            if brect.colliderect(xc):
                temp_yc = xc.copy()
                temp_yc.y -= brect.height
                if not brect.colliderect(temp_yc):
                    top = brect.top
                else:
                    return 0
            else:
                temp_yc = xc.copy()
                temp_yc.y -= brect.height
                # pygame.draw.rect(self.screen,(0,0,0),temp_yc)
                if brect.colliderect(temp_yc):
                    return 0
                
        return top
                
            
            
    def check_colliderect_blocks(self):
        dx = self.rect.x - self.rect_pre.x
        dy = self.rect.y - self.rect_pre.y
        self.rect = self.rect_pre.copy()
        rect  = self.rect_pre.copy()
        xc = pygame.Rect(rect.x + dx, rect.y, rect.width, rect.height)#앞으로
        yc = pygame.Rect(rect.x, rect.y + dy, rect.width, rect.height)#위로
        yc.centerx += int(rect.width*0.4/2)
        yc.width = int(rect.width*0.6)
        for i,block in enumerate(self.parent.group_block):
            brect = block.rect.copy()
            is_up = False
            is_down = False
                
            if brect.bottom <= self.rect_pre.top: #블럭 아래 있음
                brect.top -= self.JUMP
                brect.height += self.JUMP
                is_down = True
            else:#블럭 위에 있음
                if self.jumped:
                    brect.height += self.JUMP
                is_up = True
            # pygame.draw.rect(self.screen,(0,0,0),brect)
            if brect.colliderect(xc):
                if self.rect_pre.x < brect.x and dx<0: #왼쪽에
                    pass
                elif self.rect_pre.x > brect.x and dx>0: #오른쪽에
                    pass
                else:
                    dx = 0                    
                if not brect.colliderect(yc) and block.move_x != 0 :
                    if self.rect_pre.x < brect.x and block.direction<0: #왼쪽에
                        dx += block.direction
                    elif self.rect_pre.x > brect.x and block.direction>0: #오른쪽에
                        dx += block.direction
            
            if brect.colliderect(yc):                
                if is_down:#블럭 아래?
                    if self.jumped:                        
                        dy = 0
                        self.jump_y = abs(self.jump_y) 
                        self.rect.top =  brect.bottom+1 #블럭위에 올려 놓는다.
                        self.rect_pre = self.rect.copy()
                elif is_up:#블럭 위에?
                    self.rect.bottom =  brect.top #블럭위에 올려 놓는다.
                    self.rect_pre = self.rect.copy()
                    dy = 0
                    self.jump_y = 0
                    self.jumped = False
                        
                    # if block.move_y != 0:
                    #     dy += block.direction
                    
                    if block.move_x != 0:
                        dx += block.direction
                else:
                    dy = 0
        self.rect.x += dx
        self.rect.y += dy        
        self.rect_pre = self.rect.copy()
        return dy
        
    def game_over_process(self):
        if self.gameover:
            if self.img_gameover is not None and self.rect.bottom > 0:
                offset = self.rect.y
                offset /= 50
                offset = int(offset)
                if offset < 2:
                    offset = 2
                self.rect.y -= offset
                self.screen.blit(self.img_gameover,self.rect)
            else:
                self.game_reset(True)
            return False
        else:
            return True
        
    def check_collide_all(self):  
        weapons = pygame.sprite.spritecollide(self, self.parent.group_weapon, True)
        for weapon in weapons:
            self.weapons.append(weapon.filename)
            if self.snd_dic['weapon'] is not None:
                self.snd_dic['weapon'].play()
            
        # if pygame.sprite.spritecollide(self, self.parent.group_weapon, True):
        #     self.weapon += 1
        #     if self.snd_dic['weapon'] is not None:
        #         self.snd_dic['weapon'].play()
                
        if pygame.sprite.spritecollide(self, self.parent.group_hp, True):
            self.hp += 1
            if self.snd_dic['coin'] is not None:
                self.snd_dic['coin'].play()
                
        if pygame.sprite.spritecollide(self, self.parent.group_coin, True):
            self.score += 10
            if self.snd_dic['coin'] is not None:
                self.snd_dic['coin'].play()
        #몬스터
        if pygame.sprite.spritecollide(self, self.parent.group_monster, False):
            self.hp -= 1
            if self.snd_dic['game_over'] is not None:
                self.snd_dic['game_over'].play()
                # self.game_reset(True)
            if self.hp <= 0:
                self.gameover = True
            else:
                self.level = self.parent.map_change(self.level)
                self.image = self.get_img(self.level)
                self.rect.x,self.rect.y = self.get_position(self.level)      
                self.rect_pre = self.rect.copy()

        # 용암 충돌확인? 
        if pygame.sprite.spritecollide(self, self.parent.group_lava, False):
            self.hp -= 1
            if self.snd_dic['game_over'] is not None:
                self.snd_dic['game_over'].play()
                # self.game_reset(True)
            if self.hp <= 0:
                self.gameover = True
            else:
                self.level = self.parent.map_change(self.level)
                self.image = self.get_img(self.level)
                self.rect.x,self.rect.y = self.get_position(self.level)      
                self.rect_pre = self.rect.copy()
            
        if pygame.sprite.spritecollide(self, self.parent.group_exitDoor, False):
            if self.level >= self.parent.lastExt:
                self.MissionCompleted = True
            else:
                self.level += 1            
                self.level = self.parent.map_change(self.level)
                self.image = self.get_img(self.level)
                self.rect.x,self.rect.y = self.get_position(self.level)      
                self.rect_pre = self.rect.copy()
                self.level_real = self.level
                
    def check_level_real(self):
        if self.level_real != self.level:
            self.level_real = self.level
            self.level = self.parent.map_change(self.level)
            self.image = self.get_img(self.level)
            self.rect.x,self.rect.y = self.get_position(self.level)      
            self.rect_pre = self.rect.copy()
            self.level_real = self.level
            
    def draw_message_success(self):
        if self.MissionCompleted==False:
            if pygame.time.get_ticks() > self.gametime_tick:
                self.gametime_tick = pygame.time.get_ticks() + 10
                self.gametime += 1
            return False
        
        msg = f'Mission completed!!'
        img = self.mfont50.render(msg, True, (192,0,0))
        img.set_alpha(100)
        rect = img.get_rect()
        rect.centerx = self.screen.get_width()/2
        rect.centery = self.screen.get_height()/2-100
        self.screen.blit(img, rect)
        
        msg = f'재시작 (Click)'
        img = self.mfont40.render(msg, True, (192,0,0))
        img.set_alpha(100)
        rect = img.get_rect()
        rect.centerx = self.screen.get_width()/2
        rect.centery = self.screen.get_height()/2
        self.screen.blit(img, rect)
        
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen,(255,0,0),rect,2)
            if pygame.mouse.get_pressed()[0]:
                self.game_reset(True)
                self.level = 1            
                self.level = self.parent.map_change(self.level)
                self.image = self.get_img(self.level)
                self.rect.x,self.rect.y = self.get_position(self.level)      
                self.rect_pre = self.rect.copy()
            
        return True
        
    def draw_message(self, msg:str, color:tuple, x:int, y:int):
        msg = f'{msg}'
        img = self.mfont20.render(msg, True, color)
        self.screen.blit(img, (x, y))
    
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
        
    def set_msg_weapon(self, x=10,y=90, color = (0,0,0), text = '레벨 : '):
        self.msg_weapon_x = x
        self.msg_weapon_y = y
        self.msg_weapon_color = color
        self.msg_weapon_text = text
        
    def set_msg_hp(self, x=10,y=130, color = (0,0,0), text = 'HP : '):
        self.msg_hp_x = x
        self.msg_hp_y = y
        self.msg_hp_color = color
        self.msg_hp_text = text
        
    def set_msg_jumpcnt(self, x=10,y=170, color = (0,0,0), text = '점프 : '):
        self.msg_jumpcnt_x = x
        self.msg_jumpcnt_y = y
        self.msg_jumpcnt_color = color
        self.msg_jumpcnt_text = text
        
    def set_msg_gameTime(self, x=10,y=210, color = (0,0,0), text = '시간 : '):
        self.msg_gametime_x = x
        self.msg_gametime_y = y
        self.msg_gametime_color = color
        self.msg_gametime_text = text
        
    def draw(self):
        if self.msg_score_text is not None:
            self.draw_message(f'{self.msg_score_text}{self.score}',
                            self.msg_score_color, 
                            x=self.msg_score_x,
                            y=self.msg_score_y)
        
        if self.msg_level_text is not None:
            self.draw_message(f'{self.msg_level_text}{self.level}',
                            self.msg_level_color, 
                            x=self.msg_level_x,
                            y=self.msg_level_y)
            
        if self.msg_weapon_text is not None:
            self.draw_message(f'{self.msg_weapon_text}{len(self.weapons)}',
                            self.msg_weapon_color, 
                            x=self.msg_weapon_x,
                            y=self.msg_weapon_y)
            
        if self.msg_hp_text is not None:
            self.draw_message(f'{self.msg_hp_text}{self.hp}',
                            self.msg_hp_color, 
                            x=self.msg_hp_x,
                            y=self.msg_hp_y)
            
        if self.msg_jumpcnt_text is not None:
            self.draw_message(f'{self.msg_jumpcnt_text}{self.jump_cnt}',
                            self.msg_jumpcnt_color, 
                            x=self.msg_jumpcnt_x,
                            y=self.msg_jumpcnt_y)
            
        if self.msg_gametime_text is not None:
            self.draw_message(f'{self.msg_gametime_text}{self.gametime/100:.2f}초',
                            self.msg_gametime_color, 
                            x=self.msg_gametime_x,
                            y=self.msg_gametime_y)
            
        if self.game_over_process():
            self.check_level_real()
            if self.draw_message_success():
                pass
            else:
                self.key_pressed()        
            self.check_img_dir()
            self.rect.y += self.jump_process()
            self.check_img_screen_limit()        
            self.check_colliderect_blocks()        
            self.check_collide_all()
        
            self.screen.blit(self.image, self.rect)
        
        