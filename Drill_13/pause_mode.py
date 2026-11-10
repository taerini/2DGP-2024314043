from pico2d import *
import game_framework
import game_world

font = None

def init():
    global font
    font = load_font('C:/Windows/Fonts/malgun.ttf', 40)  # 한글이 나오는 맑은 고딕

def finish():
    global font
    del font

def update():
    pass  # 게임 월드를 업데이트하지 않으므로 화면이 멈춘다

def render():
    clear_canvas()
    game_world.render()  # 멈춘 게임 화면을 배경으로 그대로 보여줌
    draw_rectangle(250, 220, 550, 380, 255, 255, 255, 255, True)
    draw_rectangle(250, 220, 550, 380, 0, 0, 0)
    font.draw(340, 300, '정지중', (0, 0, 0))
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_mode()
