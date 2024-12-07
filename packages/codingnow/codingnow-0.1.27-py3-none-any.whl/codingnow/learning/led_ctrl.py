import os
try:
    import pygame
except:
    os.system('pip install pygame')
    import pygame
from pygame import *
# import codingnow.game
import threading
import time
try:
    import clipboard
except:
    os.system('pip install clipboard')
    import clipboard
from codingnow.learning.drawImg import *

class Led_ctrl:
    color_led = (192,0,0)
    color_background = (0,0,0)
    on_disp_grid = True
    on_disp_num = True
    on_disp_circle_mode = True
    on_all_led = False
    on_mouse_click = False
    
    led_state = {}
    mouse_click_list = []
    group_icon = pygame.sprite.Group()
    
    key_press = {
        pygame.K_UP:False,
        pygame.K_DOWN:False,
        pygame.K_LEFT:False,
        pygame.K_RIGHT:False,
    }
    key_press_state = {
        pygame.K_UP:{'pressed':False,'tick':0},
        pygame.K_DOWN:{'pressed':False,'tick':0},
        pygame.K_LEFT:{'pressed':False,'tick':0},
        pygame.K_RIGHT:{'pressed':False,'tick':0},
    }
    def __init__(self,setup,loop,colum = 8,row = 8,width = 40) -> None:
        self.setup = setup
        self.loop = loop
        self.colum = colum
        self.row = row
        self.width = width
    
        self.thread_run = True
        self.mouse_pressed = False
        self.copy_pressed = False
        
        self.rect_leds = []
        
        pygame.init()
        pygame.display.set_caption("codingnow.co.kr")
        self.screen = pygame.display.set_mode((self.colum*self.width, self.row*self.width))
        self.mfont10 = pygame.font.SysFont("malgungothic", 10)
        self.mfont20 = pygame.font.SysFont("malgungothic", 20)
        self.mfont30 = pygame.font.SysFont("malgungothic", 30)
        self.mfont40 = pygame.font.SysFont("malgungothic", 40)
        self.create_grid()
        
    def set_img(self,idex,filename):
        img_rect = pygame.Rect(0,0,self.width,self.width)
        img = DrawImg(self.screen,filename,img_rect)
        
        if idex in self.led_state:
            self.led_state[idex]['active'] = True
            self.led_state[idex]['img'] = img
            
    def set_img_all(self,filename):
        img_rect = pygame.Rect(0,0,self.width,self.width)
        img = DrawImg(self.screen,filename,img_rect)
        
        for idex in self.led_state:
            self.led_state[idex]['active'] = True
            self.led_state[idex]['img'] = img
        
    def create_grid(self):
        self.rect_leds.clear()
        self.led_state.clear()
        
        idex = 0
        for row in range(self.row):
            leds = []
            for col in range(self.colum):
                rect = pygame.Rect(col*self.width,row*self.width,self.width,self.width)
                leds.append(rect)
                self.led_state[idex] = {'active':False, 'on':False, 'color':self.color_led, 'img':None}
                idex += 1
            self.rect_leds.append(leds)
            
    # def get_key_state(self):
    #     key_press = pygame.key.get_pressed()
    #     keys = [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]
    #     for key in keys:
    #         if key_press[key]:
    #             if self.key_press_state[key]['pressed'] == False:
    #                 self.key_press_state[key]['pressed_tick'] = pygame.time.get_ticks() + 200
    #                 self.key_press_state[key]['pressed'] = True
    #                 self.key_press[key] = True
    #             else:
    #                 self.key_press[key] = False
    #                 if pygame.time.get_ticks() > self.key_press_state[key]['pressed_tick']:
    #                     self.key_press_state[key]['pressed'] = False 
    #         else:
    #             self.key_press_state[key]['pressed'] = False
    #             self.key_press_state[key]['pressed_tick'] = 0
    #             self.key_press[key] = False
                
    def get_key_press(self, key, auto=False):        
        if key not in self.key_press:
            self.key_press_state[key] = {'pressed':False,'tick':0}            
            self.key_press[key] = False
                  
        if key in self.key_press:
            if pygame.key.get_pressed()[key]:
                if auto==False:
                    self.key_press[key] = True
                elif self.key_press_state[key]['pressed'] == False:
                    self.key_press_state[key]['pressed_tick'] = pygame.time.get_ticks() + 200
                    self.key_press_state[key]['pressed'] = True
                    self.key_press[key] = True
                else:
                    self.key_press[key] = False
                    if pygame.time.get_ticks() > self.key_press_state[key]['pressed_tick']:
                        self.key_press_state[key]['pressed'] = False 
            else:
                self.key_press_state[key]['pressed'] = False
                self.key_press_state[key]['pressed_tick'] = 0
                self.key_press[key] = False
            return self.key_press[key]
            
        return False

    def draw_grid(self):
                    
        idex = 0
        if self.on_mouse_click and pygame.mouse.get_focused() and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
        else:
            mouse_pos = None
            self.mouse_pressed = False
            
        if pygame.mouse.get_pressed()[2] and len(self.mouse_click_list):
            self.mouse_click_list.clear()
            
        for y,row in enumerate(self.rect_leds):
            for x,col in enumerate(row):
                if mouse_pos is not None:
                    if col.collidepoint(mouse_pos):
                        if self.mouse_pressed==False:
                            if idex not in self.mouse_click_list:
                                self.mouse_click_list.append(idex)
                            else:
                                self.mouse_click_list.remove(idex)
                            self.mouse_pressed = True
                            self.check_clipboard()
                        
                if idex in self.mouse_click_list:
                    pygame.draw.rect(self.screen,(255,0,255),col,0)
                if self.on_disp_grid:
                    pygame.draw.rect(self.screen,(192,192,192),col,1)
                if self.on_disp_num:              
                    img = self.mfont10.render(f'{idex}', True, (0,192,192))
                    rect = img.get_rect()
                    rect.center = col.center
                    self.screen.blit(img, rect)
                
                self.draw_led(self.led_state[idex],col)
                idex += 1
                
        # print(self.mouse_click_list)

        # for rect in self.mouse_click_list:
        #     pygame.draw.rect(self.screen,(255,0,255),rect,4)
    def check_clipboard(self):
        # key_press = pygame.key.get_pressed()
        # if key_press[pygame.K_LCTRL] and key_press[pygame.K_c]:
            # if self.copy_pressed == False:
                # if len(self.mouse_click_list)>0:
                    idexs = ''
                    for idex in self.mouse_click_list:
                        if len(idexs)>0:
                            idexs += ','
                        idexs += f'{idex}'
                    clipboard.copy(idexs)
        #         self.copy_pressed = True
        # else:
        #     self.copy_pressed = False
                
    def draw_led(self,led:dict, rect: pygame.Rect):
        if led['active']==False:
            return
        
        if led['img'] is not None:
            if led['on']:
                led['img'].draw(rect)
            else:
                pass
        else:
            temp_surface = Surface((rect.width,rect.height))
            temp_surface.fill(self.color_background)
            if led['on']:
                temp_surface.set_alpha(250)
            else:
                temp_surface.set_alpha(50)
            if self.on_disp_circle_mode:
                pygame.draw.circle(temp_surface,led['color'],(rect.width/2,rect.width/2),(rect.width-2)/2)
            else:
                pygame.draw.rect(temp_surface, led['color'],(1,1,rect.width-2, rect.height-2),0)
            # 
            self.screen.blit(temp_surface,rect)
    
    def led_enable(self, *idexs, color=None):
        if color is None:
            color = self.color_led
            
        for idex in idexs:
            if idex in self.led_state:
                self.led_state[idex]['active'] = True
                self.led_state[idex]['color'] = color
                
    def led_disable(self, *idexs):
        for idex in idexs:
            if idex in self.led_state:
                self.led_state[idex]['active'] = False
                                        
    def led_on(self,*idexs):
        
        # print(idexs)
        for idex in idexs:
            if idex in self.led_state:
                self.led_state[idex]['on'] = True
                
    def led_off(self,*idexs):
        for idex in idexs:
            if idex in self.led_state:
                self.led_state[idex]['on'] = False
                
    def led_all_active(self):
        for idex in self.led_state:
            self.led_state[idex]['active'] = True
            self.led_state[idex]['color'] = self.color_led

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def run(self):
        if self.setup is not None:
            self.setup()
            
        if self.on_all_led:
            self.led_all_active()
            
        th1 = threading.Thread(target=self.display,args=[1])
        th1.start()
        
        th2 = threading.Thread(target=self.loop_thread,args=[1])
        th2.start()
        
        while self.check_quit():
            pass
        self.thread_run = False
        
    def loop_thread(self,temp):
        while self.thread_run:
            if self.loop is not None:
                self.loop()
    
    def display(self,temp):
        while self.thread_run:
            self.screen.fill(self.color_background)
            # if self.loop is not None:
            #     self.loop()
            
            self.draw_grid()
            # self.check_clipboard()
            # self.draw_led()
            pygame.display.update()
            pygame.time.Clock().tick(100)
            # time.sleep(10)

def delay(ms):
    time.sleep(ms/1000)
    
main = None
def init(setup,loop,colum = 8,row = 8,width = 40):
    global main
    main = Led_ctrl(setup,loop,colum,row,width)
    return main
    # main.run()



def set_img(idex,filename):
    global main
    main.set_img(idex,filename)

def set_img_all(filename):
    global main
    main.set_img_all(filename)

def led_on(*idexs):
    global main
    main.led_on(idexs)
    # print(idexs)
    
def led_off(*idexs):
    global main
    main.led_off(idexs)
    
def get_key_press(key, auto=False):
    global main
    return main.get_key_press(key,auto)

def led_init(on_disp_grid = True,
            on_disp_num = True,
            on_disp_circle_mode = True,
            on_all_led = True,
            color_led = (0,192,192)
            ):
    
    global main

    main.on_disp_grid = on_disp_grid
    main.on_disp_num = on_disp_num
    main.on_disp_circle_mode = on_disp_circle_mode
    main.on_all_led = on_all_led
    main.color_led = color_led