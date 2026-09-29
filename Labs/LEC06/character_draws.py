# 실습 과제 진행

import math
from pico2d import *


open_canvas(800, 600)

character = load_image('character.png')


def draw_circle():
    print("circle")
    for deg in range(0, 360, 5):
        rad=math.radians(deg)
        x=400+200*math.cos(rad)
        y=300+200*math.sin(rad)
        draw_character(x, y)
    pass

def draw_line(x1, y1, x2, y2):
    distance = math.hypot(x2 - x1, y2 - y1)
    angle = math.atan2(y2 - y1, x2 - x1)
    for d in range(0, int(distance), 5):
        x = x1 + d * math.cos(angle)
        y = y1 + d * math.sin(angle)
        draw_character(x, y)


def draw_first_line():
    print("first line")
    draw_line(111, 50, 400, 550)
    pass


def draw_second_line():
    print("second line")
    draw_line(400, 550, 689, 50)
    pass

def draw_third_line():
    print("third line")
    draw_line(111, 50, 689, 50)
    pass


def draw_triangle():
    print("triangle")
    draw_first_line()
    draw_second_line()
    draw_third_line()
    pass


def draw_top():
    print("top")
    for x in range(50, 750, 5):
        draw_character(x, 550)
    pass



def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)

def draw_right():
    print("right")
    for y in range(550, 50, -5):
        draw_character(750, y)
    pass

def draw_bottom():
    print("bottom")
    for x in range(750, 50, -5):
        draw_character(x, 50)
    pass

def draw_left():
    print("left")
    for y in range(50, 550, 5):
        draw_character(50, y)
    pass

def draw_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    pass

def exit():
    print("exit")
    pass

while True:
    draw_circle()
    draw_rectangle()
    draw_triangle()
    pass

close_canvas()