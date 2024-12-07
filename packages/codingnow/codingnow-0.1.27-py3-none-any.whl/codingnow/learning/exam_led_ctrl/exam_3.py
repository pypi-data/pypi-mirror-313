
from codingnow.learning.led_ctrl import *

colum = 9
row = 9
width = 100
leds = colum * row

heart = [31,23,24,34,43,51,59,67,21,20,28,37,47,57]

def setup():
    main.on_disp_grid = False
    main.on_disp_num = False
    main.on_disp_circle_mode = True
    # main.on_all_led = True
    main.color_led = (0,192,192)
    main.led_enable(67,57,47,37,28,20,59,51,43,34,24,31,21,23)

def loop():
    for i in heart:
        main.led_on(i)
        delay(50)

    for i in heart:
        main.led_off(i)
        delay(50)
    
main = init(setup, loop,colum,row ,width)
main.run()