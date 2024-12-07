import os
os.system('pip install pygame')
os.system('pip install clipboard')
os.system('pip install codingnow --upgrade')
import pygame

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
#마우스로 좌표 확인하기
############################## 레벨1 지도 ##################################
#블럭
#코인
#용암
#몬스터
#출구
#공격무기
############################## 레벨2 지도 ##################################
#블럭
#코인
#용암
#몬스터
#출구
#공격무기
############################## 레벨3 지도 ##################################
############################## 레벨n 지도 ##################################
##############################   플레이어   ##################################
#플레이어 넣기
#이동 속도
#게임오버 이미지
#효과음
#점수, 레벨 표시
##############################   무한반복   ##################################
while check_quit():
    screen.fill((255, 255, 255))    
    platfrom.draw()    
    pygame.display.update()
    pygame.time.Clock().tick(100)