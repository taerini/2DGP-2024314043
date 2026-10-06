from pico2d import *

WIDTH, HEIGHT = 1200, 600
CENTER_X = WIDTH // 2      # 화면 가로 중앙
GROUND_Y = 100             # 캐릭터 발이 닿는 높이
SCALE = 4                  # 확대 배율 (원본의 4배)
FRAME_TIME = 0.12          # 프레임 하나를 보여주는 시간(초)

# idle 프레임 (left, bottom, w, h) - pico2d 처럼 아래쪽 기준 좌표
IDLE_FRAMES = [(1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 28, 39), (86, 447, 30, 38),
               (118, 447, 30, 38), (150, 447, 30, 38), (182, 447, 29, 38), (211, 448, 29, 38),
               (240, 448, 29, 38), (270, 448, 24, 32), (302, 448, 29, 26)]

open_canvas(WIDTH, HEIGHT)

sprite = load_image('sonic-sprite.png')

running = True
frame_index = 0
frame_timer = 0.0           # 현재 프레임을 보여준 시간


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


def update(dt):
    # 실제 경과 시간 dt 를 쌓아서 FRAME_TIME 이 지날 때마다 다음 프레임으로
    global frame_index, frame_timer
    frame_timer += dt
    while frame_timer >= FRAME_TIME:
        frame_timer -= FRAME_TIME
        frame_index = (frame_index + 1) % len(IDLE_FRAMES)


def draw():
    clear_canvas()
    draw_frame(IDLE_FRAMES[frame_index], CENTER_X)
    update_canvas()


last_time = get_time()
while running:
    handle_events()
    now = get_time()
    update(now - last_time)
    last_time = now
    draw()
    delay(0.01)

close_canvas()
