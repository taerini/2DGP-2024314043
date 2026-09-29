# 실습 과제 진행

import math
from pico2d import *


open_canvas(800, 600)

character = load_image('character.png')


def draw_circle():
    print("circle")
    radius = 200
    circumference = 2 * math.pi * radius
    step_count = int(circumference / 5)
    for i in range(step_count):
        rad = i * (5 / radius)
        x=400+radius*math.cos(rad)
        y=300+radius*math.sin(rad)
        draw_character(x, y)
    pass

def draw_line(x1, y1, x2, y2):
    distance = math.hypot(x2 - x1, y2 - y1)
    angle = math.atan2(y2 - y1, x2 - x1)
    for d in range(0, int(distance), 5):
        x = x1 + d * math.cos(angle)
        y = y1 + d * math.sin(angle)
        draw_character(x, y)
    draw_character(x2, y2)


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
    draw_line(689, 50, 111, 50)
    pass


def draw_triangle():
    print("triangle")
    draw_first_line()
    draw_second_line()
    draw_third_line()
    pass


def draw_top():
    print("top")
    for x in range(50, 751, 5):
        draw_character(x, 550)
    pass



def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)
    if not gameExit():
        close_canvas()
        exit()

def draw_right():
    print("right")
    for y in range(550, 49, -5):
        draw_character(750, y)
    pass

def draw_bottom():
    print("bottom")
    for x in range(750, 49, -5):
        draw_character(x, 50)
    pass

def draw_left():
    print("left")
    for y in range(50, 551, 5):
        draw_character(50, y)
    pass

def draw_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    pass

def gameExit():
    print("gameExit")
    events=get_events()
    for event in events:
        if event.type==SDL_KEYDOWN and event.key==SDLK_q:
            return False
    return True


while gameExit():
    draw_circle()
    draw_rectangle()
    draw_triangle()
    pass

close_canvas()