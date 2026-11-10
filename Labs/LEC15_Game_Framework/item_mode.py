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
    pass  # 아이템 선택 중에는 게임 월드를 업데이트하지 않음

def render():
    clear_canvas()
    game_world.render()  # 멈춘 게임 화면을 배경으로 그대로 보여줌
    image.draw(400, 300)  # 화면 가운데에 아이템 선택창
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()

