# 실습 과제 진행
from pico2d import *

open_canvas(800, 600)

character = load_image('character.png')


def move_circle():
    pass

def move_triangle():
    pass

def move_rectangle():
    pass

while True:
    clear_canvas()
    move_circle()
    move_triangle()
    move_rectangle()
    update_canvas()
    get_events()

close_canvas()