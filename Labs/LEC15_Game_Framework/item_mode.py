from pico2d import *
import game_framework
import game_world
import play_mode

image = None

# 누른 숫자 키 -> 소년이 갖게 될 아이템
ITEM_KEYS = {
    SDLK_0: None,       # 공 없음
    SDLK_1: 'Ball',     # 작은 공
    SDLK_2: 'BigBall',  # 큰 공
}

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
        elif event.type == SDL_KEYDOWN and event.key in ITEM_KEYS:
            play_mode.boy.item = ITEM_KEYS[event.key]
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_i, SDLK_ESCAPE):
            game_framework.pop_mode()  # 선택하지 않고 닫기

