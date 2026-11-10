from pico2d import *
import game_framework

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
    pass

def handle_events():
    pass
