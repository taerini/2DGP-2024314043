from pico2d import *

WIDTH, HEIGHT = 1200, 600
CENTER_X = WIDTH // 2      # 화면 가로 중앙
GROUND_Y = 100             # 캐릭터 발이 닿는 높이
SCALE = 4                  # 확대 배율 (원본의 4배)

open_canvas(WIDTH, HEIGHT)

sprite = load_image('sonic-sprite.png')

running = True


def handle_events():
    # 창의 X 버튼이나 ESC 키를 누르면 running 을 False 로 바꿔 종료
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw():
    clear_canvas()
    # 확인용: idle 첫 프레임 (left, bottom, w, h) = (1, 447, 29, 39) 를 4배로 중앙에
    sprite.clip_draw(1, 447, 29, 39, CENTER_X, GROUND_Y + 39 * SCALE / 2, 29 * SCALE, 39 * SCALE)
    update_canvas()


while running:
    handle_events()
    draw()
    delay(0.01)

close_canvas()
