from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

# 이미지 불러오기 (한 번만)
boy = load_image('animation_sheet.png')
tuk = load_image('TUK_GROUND.png')

# 동작 이름: (시트에서 줄 위치, 프레임 수)
ANIMATIONS = {
    'run_right':  (100, 8),
    'run_left':   (0,   8),
    'idle_right': (300, 8),
    'idle_left':  (200, 8),
}

running = True
dir_x = 0             # 좌우 방향: -1(왼쪽), 0(정지), 1(오른쪽)
dir_y = 0             # 상하 방향: -1(아래), 0(정지), 1(위)
x = 400               # 가로 위치
y = 300               # 세로 위치
speed = 5             # 이동 속도
frame = 0             # 지금 몇 번째 그림인지
facing = 1            # 마지막으로 바라본 방향: 1(오른쪽), -1(왼쪽)
state = 'idle_right'  # 지금 동작


def handle_event():
    global running
    global dir_x, dir_y

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                dir_x = dir_x - 1
            elif event.key == SDLK_RIGHT:
                dir_x = dir_x + 1
            elif event.key == SDLK_UP:
                dir_y = dir_y + 1
            elif event.key == SDLK_DOWN:
                dir_y = dir_y - 1
            elif event.key == SDLK_ESCAPE:
                running = False

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                dir_x = dir_x + 1
            elif event.key == SDLK_RIGHT:
                dir_x = dir_x - 1
            elif event.key == SDLK_UP:
                dir_y = dir_y - 1
            elif event.key == SDLK_DOWN:
                dir_y = dir_y + 1


def update():
    global x, y, frame, facing, state

    # 1. 위치 이동
    x = x + dir_x * speed
    y = y + dir_y * speed

    # 2. 좌우로 움직이고 있으면 바라보는 방향 기억
    if dir_x != 0:
        facing = dir_x

    # 3. 움직이는 중인지 확인
    if dir_x != 0 or dir_y != 0:
        moving = True
    else:
        moving = False

    # 4. 바라보는 방향 이름 정하기
    if facing == 1:
        side = 'right'
    else:
        side = 'left'

    # 5. 상태 이름 정하기
    if moving == True:
        new_state = 'run_' + side
    else:
        new_state = 'idle_' + side

    # 6. 동작이 바뀌었으면 프레임을 처음부터
    if new_state != state:
        state = new_state
        frame = 0

    # 7. 다음 프레임으로 넘기기
    animation = ANIMATIONS[state]     # 예: (100, 8)
    frame_count = animation[1]        # 두 번째 값 = 프레임 수
    frame = frame + 1
    if frame >= frame_count:          # 마지막 장을 넘어가면
        frame = 0                     # 처음으로


def draw():
    clear_canvas()

    # 배경 먼저
    tuk.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)

    # 캐릭터는 배경 위에
    animation = ANIMATIONS[state]     # 예: (100, 8)
    row = animation[0]                # 첫 번째 값 = 시트에서 줄 위치
    boy.clip_draw(frame * 100, row, 100, 100, x, y)

    update_canvas()


while running:
    handle_event()
    update()
    draw()
    delay(0.05)

close_canvas()