from pico2d import *
import game_framework
import game_world

image = None

def init():
    global image
    image = load_image('item_select.png')

def finish():
    global image
    del image

def update():
    pass

def render():
    clear_canvas()
    game_world.render()  # 멈춘 게임 화면을 배경으로 그대로 보여줌
    update_canvas()

def handle_events():
    pass
