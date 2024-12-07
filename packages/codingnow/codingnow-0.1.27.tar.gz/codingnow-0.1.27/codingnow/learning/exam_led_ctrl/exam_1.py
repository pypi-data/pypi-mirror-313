
from codingnow.learning.led_ctrl import *

colum = 9
row = 9
width = 100
leds = colum * row

def setup():
    # main.on_disp_grid = False
    # main.on_disp_num = False
    main.on_disp_circle_mode = True
    main.on_all_led = False
    main.color_led = (0,192,192)
    main.led_enable(0,1,color=(0,0,255))
    main.led_enable(2,3)

def loop():
    main.led_on(0,1)
    delay(500)
    main.led_off(0,1)
    delay(500)
    main.led_on(2,3)
    delay(500)
    main.led_off(2,3)
    delay(500)
    
main = init(setup, loop,colum,row ,width)
main.run()