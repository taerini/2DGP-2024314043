# 실습 과제 진행

import math
from pico2d import *


open_canvas(800, 600)

character = load_image('character.png')

STEP = 5
LEFT, RIGHT = 50, 750
BOTTOM, TOP = 50, 550
CENTER_X, CENTER_Y = 400, 300
CIRCLE_RADIUS = 200
TRI_LEFT, TRI_RIGHT = 111, 689
TRI_APEX_X, TRI_APEX_Y = 400, 550


def draw_circle():
    print("circle")
    circumference = 2 * math.pi * CIRCLE_RADIUS
    step_count = int(circumference / STEP)
    for i in range(step_count):
        rad = i * (STEP / CIRCLE_RADIUS)
        x=CENTER_X+CIRCLE_RADIUS*math.cos(rad)
        y=CENTER_Y+CIRCLE_RADIUS*math.sin(rad)
        draw_character(x, y)
    draw_character(CENTER_X + CIRCLE_RADIUS, CENTER_Y)
    pass

def draw_line(x1, y1, x2, y2):
    distance = math.hypot(x2 - x1, y2 - y1)
    angle = math.atan2(y2 - y1, x2 - x1)
    for d in range(0, int(distance), STEP):
        x = x1 + d * math.cos(angle)
        y = y1 + d * math.sin(angle)
        draw_character(x, y)
    draw_character(x2, y2)


def draw_first_line():
    print("first line")
    draw_line(TRI_LEFT, BOTTOM, TRI_APEX_X, TRI_APEX_Y)
    pass


def draw_second_line():
    print("second line")
    draw_line(TRI_APEX_X, TRI_APEX_Y, TRI_RIGHT, BOTTOM)
    pass

def draw_third_line():
    print("third line")
    draw_line(TRI_RIGHT, BOTTOM, TRI_LEFT, BOTTOM)
    pass


def draw_triangle():
    print("triangle")
    draw_first_line()
    draw_second_line()
    draw_third_line()
    pass


def draw_top():
    print("top")
    for x in range(LEFT, RIGHT + 1, STEP):
        draw_character(x, TOP)
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
    for y in range(TOP, BOTTOM - 1, -STEP):
        draw_character(RIGHT, y)
    pass

def draw_bottom():
    print("bottom")
    for x in range(RIGHT, LEFT - 1, -STEP):
        draw_character(x, BOTTOM)
    pass

def draw_left():
    print("left")
    for y in range(BOTTOM, TOP + 1, STEP):
        draw_character(LEFT, y)
    pass

def draw_rectangle():
    print("rectangle")
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()
    pass

def gameExit():
    events=get_events()
    for event in events:
        if event.type==SDL_KEYDOWN and event.key in (SDLK_q, SDLK_ESCAPE):
            return False
    return True


while gameExit():
    draw_circle()
    draw_rectangle()
    draw_triangle()
    pass

close_canvas()