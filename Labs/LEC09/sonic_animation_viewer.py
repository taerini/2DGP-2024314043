from pico2d import *

WIDTH, HEIGHT = 1200, 600
CENTER_X = WIDTH // 2      # 화면 가로 중앙
GROUND_Y = 100             # 캐릭터 발이 닿는 높이
SCALE = 4                  # 확대 배율 (원본의 4배)
REPEAT = 5                 # 동작 하나를 반복 재생하는 횟수
PAUSE_TIME = 1.0           # 반복이 끝난 뒤 정지하는 시간(초)

# 동작 목록: 이름, 프레임 (left, bottom, w, h) 목록, 프레임 하나를 보여주는 시간(초)
# 프레임 좌표는 pico2d 처럼 아래쪽 기준
ACTIONS = [
    {'name': 'idle', 'frame_time': 0.12,
     'frames': [(1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 28, 39), (86, 447, 30, 38),
                (118, 447, 30, 38), (150, 447, 30, 38), (182, 447, 29, 38), (211, 448, 29, 38),
                (240, 448, 29, 38), (270, 448, 24, 32), (302, 448, 29, 26)]},
]

open_canvas(WIDTH, HEIGHT)

sprite = load_image('sonic-sprite.png')

running = True
action_index = 0            # 지금 재생 중인 동작 번호
frame_index = 0
repeat_count = 0            # 지금 동작을 끝까지 재생한 횟수
frame_timer = 0.0           # 현재 프레임을 보여준 시간
pausing = False             # True 면 정지 구간 (마지막 프레임 유지)
pause_timer = 0.0           # 정지한 시간


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


def start_action(index):
    # index 번 동작을 처음부터 재생하도록 상태를 초기화
    global action_index, frame_index, repeat_count, frame_timer, pausing, pause_timer
    action_index = index
    frame_index = 0
    repeat_count = 0
    frame_timer = 0.0
    pausing = False
    pause_timer = 0.0


def update(dt):
    # 실제 경과 시간 dt 를 쌓아서 frame_time 이 지날 때마다 다음 프레임으로
    # 마지막 프레임을 보여준 뒤에는 1회 재생 완료, REPEAT 회가 끝나면 PAUSE_TIME 동안 정지
    # 정지 중에도 이 함수는 매 화면 불리므로 이벤트 처리와 화면 갱신은 계속됨
    global frame_index, frame_timer, repeat_count, pausing, pause_timer
    action = ACTIONS[action_index]
    if pausing:
        pause_timer += dt
        if pause_timer >= PAUSE_TIME:
            start_action(action_index)   # 아직 동작이 하나뿐이라 같은 동작을 다시 재생
        return
    frame_timer += dt
    while frame_timer >= action['frame_time']:
        frame_timer -= action['frame_time']
        if frame_index == len(action['frames']) - 1:
            repeat_count += 1
            if repeat_count >= REPEAT:
                pausing = True
                return
            frame_index = 0
        else:
            frame_index += 1


def draw():
    clear_canvas()
    draw_frame(ACTIONS[action_index]['frames'][frame_index], CENTER_X)
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
