
from codingnow.learning.led_ctrl import *

colum = 9
row = 9
width = 100
leds = colum * row

# heart = [31,23,24,34,43,51,59,67,21,20,28,37,47,57]
man01 = [4,12,22,14,31,40,49,57,65,73,59,69,79,32,33,34,30,29,28]
man02 = [4,12,22,14,31,40,49,57,65,73,59,69,79,32,33,30,29,19,43]
man03 = [4,12,22,14,31,40,49,57,65,73,59,69,79,32,33,30,29,37,25]

def setup():
    main.on_disp_grid = False
    main.on_disp_num = False
    main.on_disp_circle_mode = True
    main.on_all_led = True
    main.color_led = (0,192,192)
    # main.led_enable(67,57,47,37,28,20,59,51,43,34,24,31,21,23)

def loop():
    pass

    # for i in man01:
    #     main.led_on(i)
    # delay(500)
    # for i in man01:
    #     main.led_off(i)
    
    for i in man02:
        main.led_on(i)
    delay(500)
    for i in man02:
        main.led_off(i)
        
    for i in man03:
        main.led_on(i)
    delay(500)
    for i in man03:
        main.led_off(i)
        
main = init(setup, loop,colum,row ,width)
main.run()