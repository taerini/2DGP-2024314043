from pico2d import *

WIDTH, HEIGHT = 1200, 600

open_canvas(WIDTH, HEIGHT)

running = True


def handle_events():
    # 창의 X 버튼이나 ESC 키를 누르면 running 을 False 로 바꿔 종료
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


while running:
    handle_events()

close_canvas()
