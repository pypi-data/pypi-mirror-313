
from codingnow.learning.led_ctrl import *

colum = 9
row = 9
width = 100
leds = colum * row

def setup():
    # main.on_disp_grid = False
    # main.on_disp_num = False
    main.on_disp_circle_mode = True
    # main.on_all_led = True
    main.color_led = (0,192,192)
    main.led_enable(11)

def loop():
    main.led_on(11)
    delay(50)

    main.led_off(11)
    delay(50)

main = init(setup, loop,colum,row ,width)
main.run()