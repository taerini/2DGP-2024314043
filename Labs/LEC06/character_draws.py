# 실습 과제 진행

import math
from pico2d import *



open_canvas(800, 600)

character = load_image('character.png')


def move_circle():
    print("circle")
    for deg in range(0, 360, 5):
        rad=math.radians(deg)
        x=400+200*math.cos(rad)
        y=300+200*math.sin(rad)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    pass

def move_triangle():
    print("triangle")
    pass

def move_rectangle():
    print("rectangle")
    pass

while True:
    move_circle()
    move_triangle()
    move_rectangle()
    pass

close_canvas()