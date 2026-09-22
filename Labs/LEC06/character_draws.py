# 실습 과제 진행
from pico2d import *

open_canvas(800, 600)


def move_circle():
    print("circle")
    pass

def move_triangle():
    print("triangle")
    pass

def move_rectangle():
    print("rectangle")
    pass

while True:
    clear_canvas()
    move_circle()
    move_triangle()
    move_rectangle()
    update_canvas()
    get_events()

close_canvas()