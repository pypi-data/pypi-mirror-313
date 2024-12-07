import pygame
import pygame.display
import pygame.time
import pygame.image
import pygame.transform
import pygame.event

from codingnow.game.platform.platformGame import *

def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

pygame.init()
pygame.display.set_caption("codingnow.co.kr")
screen = pygame.display.set_mode((600, 600))

platfrom = PlatformGame(screen)#플렛폼 게임 생성
#배경넣기
platfrom.add_bg_image('bg.png')
#마우스로 좌표 확인하기
platfrom.on_mouse_point = True
############################## 레벨1 지도 ##################################
#블럭(사이즈 : 60x30)
platfrom.add_map_block(level=1,filename='platform.png',x=0,y=570,move_x=0,move_y=0)
platfrom.add_map_block(level=1,filename='platform.png',x=60,y=570,move_x=0,move_y=0)
platfrom.add_map_block(level=1,filename='platform.png',x=120,y=540,move_x=0,move_y=0)
platfrom.add_map_block(level=1,filename='platform.png',x=180,y=510,move_x=0,move_y=0)
#코인
platfrom.add_map_coin(level=1,filename='coin.png',x=60,y=400)
platfrom.add_map_coin(level=1,filename='coin.png',x=120,y=400)
platfrom.add_map_coin(level=1,filename='coin.png',x=180,y=400)
platfrom.add_map_coin(level=1,filename='coin.png',x=260,y=400)
#용암
platfrom.add_map_lava(level=1,filename='lava.png',x=260,y=570,num=5)
#몬스터
platfrom.add_map_mons(level=1,filename='monster.png',x=260,y=510)
#출구
platfrom.add_map_exit(level=1,filename='exit.png',x=320,y=510)
#공격무기
platfrom.add_map_weapon(level=1,filename='bullet.png',x= 60,y=400)
platfrom.add_map_weapon(level=1,filename='bullet.png',x=160,y=440)
platfrom.add_map_weapon(level=1,filename='bullet.png',x=250,y=380)
############################## 레벨2 지도 ##################################
#블럭
#코인
#용암
#몬스터
#출구
#공격무기
##############################   플레이어   ##################################
#플레이어 넣기
player = platfrom.add_player('img1.png')
#이동 속도
player.speed = 2
#게임오버 이미지
#효과음
#점수, 레벨 표시
##############################   무한반복   ##################################
while check_quit():
    screen.fill((255, 255, 255))    
    platfrom.draw()    
    pygame.display.update()
    pygame.time.Clock().tick(100)