
from codingnow.learning.led_ctrl import *

colum = 20
row = 10
width = 20
leds = colum * row

def setup():
    main.on_disp_grid = False
    main.on_disp_num = False
    main.on_disp_circle_mode = True
    main.on_all_led = True
    main.color_led = (0,192,192)

def loop():
    for i in range(leds):
        main.led_on(i)
        delay(50)

    for i in range(leds):
        main.led_off(i)
        delay(50)

main = init(setup, loop,colum,row ,width)
main.run()