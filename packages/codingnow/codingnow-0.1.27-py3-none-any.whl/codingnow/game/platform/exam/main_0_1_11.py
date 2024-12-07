
import os
os.system('pip install codingnow --upgrade')
from codingnow.game.platform.platformGame import *

pygame.init()
pygame.display.set_caption("codingnow.co.kr")
screen = pygame.display.set_mode((600, 600))
    
##################### 플렛폼 게임 생성(코딩나우 패키지) #####################
# 1) 플렛폼 생성
platfrom = PlatformGame(screen)
# 2) 배경넣기
platfrom.add_bg_image('bg.png')
# 3) 마우스로 좌표 확인하기
platfrom.on_mouse_point = True
#------------------------------ 레벨1 지도
# 1) 블럭(사이즈 : 60x30)
platfrom.add_map_block(level=1,filename='platform.png',x=90,y=570,move_x=0,move_y=0,num=1)
platfrom.add_map_block(level=1,filename='platform.png',x=130,y=540,move_x=0,move_y=0,num=5)
platfrom.add_map_block(level=1,filename='platform.png',x=240,y=480,move_x=1,move_y=0,num=1)
platfrom.add_map_block(level=1,filename='platform.png',x=360,y=440,move_x=0,move_y=1,num=1)
# 2) 코인
platfrom.add_map_coin(level=1,filename='coin.png',x= 60,y=400)
platfrom.add_map_coin(level=1,filename='coin.png',x=120,y=400)
platfrom.add_map_coin(level=1,filename='coin.png',x=180,y=400)
platfrom.add_map_coin(level=1,filename='coin.png',x=260,y=400)
# 3) 용암
platfrom.add_map_lava(level=1,filename='lava.png',x=260,y=510,num=5)
# 4) 몬스터
platfrom.add_map_mons(level=1,filename='monster.png',x=470,y=400)
# 5) 공격무기
platfrom.add_map_weapon(level=1,filename='bullet.png',x= 60,y=400)
platfrom.add_map_weapon(level=1,filename='bullet.png',x=160,y=440)
platfrom.add_map_weapon(level=1,filename='bullet.png',x=250,y=380)
platfrom.add_map_weapon(level=1,filename='bullet.png',x=350,y=390)
# 6) 출구
platfrom.add_map_exit(level=1,filename='exit.png',x=430,y=320)

#------------------------------ 레벨2 지도
# 1) 블럭(사이즈 : 60x30)
platfrom.add_map_block(level=2,filename='platform.png',x=90,y=570,move_x=0,move_y=0,num=1)
platfrom.add_map_block(level=2,filename='platform.png',x=130,y=540,move_x=0,move_y=0,num=5)
platfrom.add_map_block(level=2,filename='platform.png',x=240,y=480,move_x=1,move_y=0,num=1)
platfrom.add_map_block(level=2,filename='platform.png',x=360,y=440,move_x=0,move_y=1,num=1)
# 2) 코인
platfrom.add_map_coin(level=2,filename='coin.png',x= 60,y=400)
platfrom.add_map_coin(level=2,filename='coin.png',x=120,y=400)
platfrom.add_map_coin(level=2,filename='coin.png',x=180,y=400)
platfrom.add_map_coin(level=2,filename='coin.png',x=260,y=400)
# 3) 용암
platfrom.add_map_lava(level=2,filename='lava.png',x=260,y=510,num=5)
# 4) 몬스터
platfrom.add_map_mons(level=2,filename='monster.png',x=470,y=400)
# 5) 공격무기
platfrom.add_map_weapon(level=2,filename='bullet.png',x= 60,y=400)
platfrom.add_map_weapon(level=2,filename='bullet.png',x=160,y=440)
platfrom.add_map_weapon(level=2,filename='bullet.png',x=250,y=380)
platfrom.add_map_weapon(level=2,filename='bullet.png',x=350,y=390)
# 6) 출구
platfrom.add_map_exit(level=2,filename='exit.png',x=430,y=320)

#------------------------------ 레벨3 지도
# 1) 블럭(사이즈 : 60x30)
platfrom.add_map_block(level=3,filename='platform.png',x=90,y=570,move_x=0,move_y=0,num=1)
platfrom.add_map_block(level=3,filename='platform.png',x=130,y=540,move_x=0,move_y=0,num=5)
platfrom.add_map_block(level=3,filename='platform.png',x=240,y=480,move_x=1,move_y=0,num=1)
platfrom.add_map_block(level=3,filename='platform.png',x=360,y=440,move_x=0,move_y=1,num=1)
# 2) 코인
platfrom.add_map_coin(level=3,filename='coin.png',x= 60,y=400)
platfrom.add_map_coin(level=3,filename='coin.png',x=120,y=400)
platfrom.add_map_coin(level=3,filename='coin.png',x=180,y=400)
platfrom.add_map_coin(level=3,filename='coin.png',x=260,y=400)
# 3) 용암
platfrom.add_map_lava(level=3,filename='lava.png',x=260,y=510,num=5)
# 4) 몬스터
platfrom.add_map_mons(level=3,filename='monster.png',x=470,y=400)
# 5) 공격무기
platfrom.add_map_weapon(level=3,filename='bullet.png',x= 60,y=400)
platfrom.add_map_weapon(level=3,filename='bullet.png',x=160,y=440)
platfrom.add_map_weapon(level=3,filename='bullet.png',x=250,y=380)
platfrom.add_map_weapon(level=3,filename='bullet.png',x=350,y=390)
# 6) 출구
platfrom.add_map_exit(level=3,filename='exit.png',x=430,y=320)
##############################   플레이어   ##################################
# 1) 생성하기
player = platfrom.add_player('img1.png')
# 2) 이동 속도
player.speed = 2
# 3) 시작 위치
player.set_position(level=1,x=50,y=490)
player.set_position(level=2,x=300,y=320)
player.set_position(level=3,x=180,y=440)

# 4) 점프 레벨
player.JUMP = 15

# 5) 레벨마다 이미지 
player.set_img(level=1,filename='img1.png',width=60,height=60)
player.set_img(level=2,filename='player_army.png',width=30,height=30)
player.set_img(level=3,filename='player_police.png')

# 6) 게임오버 이미지
player.set_gameover_image('ghost.png')

# 7) 효과음
player.set_snd_weapon('coin.wav')
player.set_snd_coin('coin.wav')
player.set_snd_jump('jump.wav')
player.set_snd_monster('monster.wav')
player.set_snd_game_over('game_over.wav')

# 8) 점수, 레벨 표시
player.set_msg_score(x=10,y=10,color=(0,0,0),text='점수 : ')
player.set_msg_level(x=10,y=30,color=(0,0,0),text='레벨 : ')
player.set_msg_weapon(x=10,y=50,color=(0,0,0),text='무기 : ')

##############################   무한반복   ##################################
while platfrom.check_quit():
    screen.fill((255, 255, 255))    
    platfrom.draw()    
    pygame.display.update()
    pygame.time.Clock().tick(100)
    