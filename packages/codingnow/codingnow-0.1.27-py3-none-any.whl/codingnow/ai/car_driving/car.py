import pygame
from pygame import Surface
import math

class Car:

    def __init__(self,screen: Surface,cx,cy) -> None:
        self.screen = screen        
        img = self.draw_car_top_view()
        self.image_src = pygame.transform.scale(img,(60,150))
        self.image = self.image_src
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        # car_pos = [screen_width // 2, screen_height // 2]
        self.car_angle = 90
        self.car_speed = 5  # 자동차가 움직이는 속도
        
        self.car_pos = [cx, cy]
        self.is_coli = False
        self.is_coli_left = False

    def draw_car_top_view(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        DARK_GRAY = (50, 50, 50)
        LIGHT_GRAY = (150, 150, 150)
        temp_surface = Surface((200+20,400))
        temp_surface.fill((255,255,255))
        # 차체 (빨간색 몸체)
        #200,150
        rect_body = pygame.Rect(0,0,200,400)
        rect_body.centerx = temp_surface.get_width()/2
        rect_body.centery = temp_surface.get_height()/2
        pygame.draw.rect(temp_surface, RED, rect_body, 0, border_radius=60)

        # # 앞/뒷 창문 (어두운 회색)
        rect_win = pygame.Rect(0,0,160,80)
        rect_win.centerx = rect_body.centerx
        rect_win.centery = rect_body.centery - rect_body.height/6
        pygame.draw.rect(temp_surface, DARK_GRAY, rect_win, 0, border_radius=20)  # 앞창문
        rect_win.centery = rect_body.centery + rect_body.height/4
        pygame.draw.rect(temp_surface, DARK_GRAY, rect_win, 0, border_radius=20)  # 뒷창문

        # # 바퀴
        rect_wheel = pygame.Rect(0,0,10,80)
        rect_wheel.right = rect_body.left
        rect_wheel.centery = rect_body.centery - rect_body.height/5
        pygame.draw.rect(temp_surface, BLACK, rect_wheel, 0)  # 왼쪽
        rect_wheel.left = rect_body.right
        pygame.draw.rect(temp_surface, BLACK, rect_wheel, 0)  # 오른쪽
        
        rect_wheel.right = rect_body.left
        rect_wheel.centery = rect_body.centery + rect_body.height/4
        pygame.draw.rect(temp_surface, BLACK, rect_wheel, 0)  # 왼쪽
        rect_wheel.left = rect_body.right
        pygame.draw.rect(temp_surface, BLACK, rect_wheel, 0)  # 오른쪽
        return temp_surface
        
    def update(self,left=False, right=False,go=False, back=False):
        # 키 입력 처리 (왼쪽, 오른쪽 방향키로 회전)
        car_pos = [self.car_pos[0], self.car_pos[1]]
        car_angle = self.car_angle
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or left:
            car_angle += 45
        if keys[pygame.K_RIGHT] or right:
            car_angle -= 45
        if keys[pygame.K_UP] or go:
            car_pos[0] += self.car_speed * math.cos(math.radians(-car_angle))
            car_pos[1] += self.car_speed * math.sin(math.radians(-car_angle))
        if keys[pygame.K_DOWN] or back:
            car_pos[0] -= self.car_speed * math.cos(math.radians(-car_angle))
            car_pos[1] -= self.car_speed * math.sin(math.radians(-car_angle))
            
        image = pygame.transform.rotate(self.image_src, car_angle-90)
        rect = image.get_rect(center=(car_pos[0], car_pos[1]))
        
        if (rect.x < 0):
            return True
        elif (rect.y < 0):
            return True
        elif (rect.right > self.screen.get_width()):
            return True
        elif (rect.bottom > self.screen.get_height()):
            return True
        else:
            self.car_pos = [car_pos[0], car_pos[1]]
            self.car_angle = car_angle
            self.image = image
            self.rect = rect
        return False
    
    def draw(self):
        if self.is_coli:
            if self.is_coli_left:
                if self.update(right=True):
                    self.is_coli_left = False
                else:
                    self.is_coli = False
            else:
                if self.update(left=True):
                    self.is_coli_left = True
                else:
                    self.is_coli = False                
        else:
            if self.update(go=True):
                self.update(back=True)
                self.is_coli = True
            
        self.screen.blit(self.image,self.rect)