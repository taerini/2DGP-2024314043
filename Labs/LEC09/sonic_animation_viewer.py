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


def draw_frame(frame, x, y=GROUND_Y):
    # frame = (left, bottom, w, h) 영역을 SCALE 배로 확대해 그림
    # 프레임마다 크기가 달라도 아래 변 중앙이 (x, y)에 오도록 중심 위치를 계산
    left, bottom, w, h = frame
    sprite.clip_draw(left, bottom, w, h, x, y + h * SCALE / 2, w * SCALE, h * SCALE)


def draw():
    clear_canvas()
    # 확인용: 크기가 다른 idle 프레임 두 장의 발 높이 비교
    draw_frame((1, 447, 29, 39), CENTER_X - 200)
    draw_frame((302, 448, 29, 26), CENTER_X + 200)
    update_canvas()


while running:
    handle_events()
    draw()
    delay(0.01)

close_canvas()
