# 소닉 애니메이션 뷰어 (장면 시나리오)
# sonic-sprite.png 의 줄별 동작으로 정해진 장면을 차례로 한 번 재생하고 마지막 포즈에서 멈춤
# 종료: 창 닫기 버튼 또는 ESC

from pico2d import *
import os
import pico2d

WIDTH, HEIGHT = 1200, 600
CENTER_X = WIDTH // 2      # 화면 가로 중앙
GROUND_Y = 100             # 캐릭터 발이 닿는 높이
START_X = 100              # 왼쪽 아래 시작점의 가로 위치
SCALE = 4                  # 기본 확대 배율 (원본의 4배)
BALL_FRAME_TIME = 0.06     # 장면 밖에서 공(기다림, 날아감) 프레임 하나를 보여주는 시간(초)
WAIT_BOUNCE = 16           # 공이 기다리는 동안 튕기는 높이(px)
WAIT_PERIOD = 0.36         # 기다리는 동안 한 번 튕기는 시간(초)
FLY_TO_CORNER = 0.5        # 찬 공이 오른쪽 위 모서리까지 날아가는 시간(초)
FLY_TO_TOP = 0.6           # 모서리에서 튕겨 소닉 머리 위 화면 밖까지 날아가는 시간(초)

# 줄별 프레임 (left, bottom, w, h) 목록 - pico2d 처럼 아래쪽 기준 좌표, 위에서부터 1~10번째 줄
FRAMES = {
    'idle': [(1, 447, 29, 39), (31, 447, 26, 38), (58, 447, 28, 39), (86, 447, 30, 38),
             (118, 447, 30, 38), (150, 447, 30, 38), (182, 447, 29, 38), (211, 448, 29, 38),
             (240, 448, 29, 38), (270, 448, 24, 32), (302, 448, 29, 26)],
    'walk': [(8, 408, 26, 37), (37, 408, 27, 37), (65, 407, 31, 38), (97, 408, 37, 37),
             (135, 410, 32, 35), (170, 408, 32, 38), (206, 408, 26, 38), (238, 408, 24, 37),
             (263, 408, 30, 37), (295, 408, 36, 37), (334, 409, 32, 36), (370, 408, 29, 38)],
    'run': [(1, 361, 33, 40), (39, 362, 35, 39), (89, 362, 35, 38), (130, 362, 34, 42),
            (181, 362, 34, 41), (228, 363, 33, 40)],
    'spin': [(1, 326, 29, 30), (35, 327, 29, 31), (67, 327, 30, 29), (98, 327, 31, 29),
             (131, 327, 29, 30), (162, 326, 29, 31), (193, 326, 30, 29), (230, 326, 31, 29),
             (268, 325, 30, 30)],
    'ball': [(1, 292, 30, 27), (36, 292, 29, 27), (70, 292, 29, 27), (105, 292, 29, 27),
             (139, 292, 29, 27), (174, 292, 29, 27)],
    'dash': [(1, 251, 29, 35), (36, 251, 30, 35), (74, 251, 31, 35), (111, 251, 31, 36),
             (149, 251, 30, 35), (186, 251, 31, 36)],
    'peel_out': [(1, 207, 29, 35), (36, 207, 30, 35), (72, 208, 39, 31), (123, 208, 39, 32),
                 (172, 208, 39, 31), (218, 208, 38, 32)],
    'leap': [(1, 154, 24, 45), (31, 154, 29, 44), (65, 154, 20, 44), (90, 155, 25, 43),
             (119, 155, 25, 43), (149, 154, 20, 44), (184, 156, 40, 28), (232, 157, 39, 27)],
    'skid': [(1, 108, 27, 38), (31, 110, 31, 36), (64, 110, 31, 36), (99, 110, 33, 38),
             (136, 110, 32, 36), (176, 110, 33, 36), (217, 110, 33, 36), (254, 111, 33, 36)],
    'pose': [(6, 56, 34, 40), (49, 56, 34, 43), (96, 59, 23, 39), (125, 59, 23, 39)],
}

# 장면 목록 (차례로 한 번씩 재생)
# actor: 'a' 는 처음 소닉(나중에 공), 'b' 는 나중에 등장하는 소닉
# frames: FRAMES 의 줄 이름, frame_time: 프레임 하나를 보여주는 시간(초), duration: 장면 시간(초)
# x, y, scale: (시작값, 끝값) - 장면 동안 경과 시간 비율로 보간, 시작값이 None 이면 앞 장면에서 이어받음
# direction: 1 이면 오른쪽, -1 이면 왼쪽(그림 좌우 반전), 'auto' 면 x 끝값을 향하는 쪽
# once: True 면 프레임을 한 번만 재생 (기본은 장면이 끝날 때까지 반복)
# bounces: 튕김마다 최고 높이(px) 목록 - 장면 시간을 똑같이 나눠 차례로 튕김
# ball_wait: True 면 장면이 끝난 뒤 공(소닉 A)이 그 자리에서 작게 튕기며 기다림
# frame_order: 줄의 프레임 중 쓸 번호 목록 (없으면 줄 전체를 순서대로)
# x_path: [(x, 프레임 수), ...] - 시작 위치(앞 장면에서 이어받음)에서 x 까지 그 프레임 수만큼의 시간 동안 직선 이동
# kick: (달려가는 줄, 달리는 프레임 시간) - 정해진 시간 대신 speed(px/s) 로 달려가 공 앞에 멈춘 뒤
#       frames 줄을 한 번 재생하며 kick_frame 번째 그림에서 공을 참, 공이 사라지면 장면 끝
# leap: (올라가는 시간, 떨어지는 시간, 최고 높이, 떨어지며 오른쪽으로 가는 거리)
#       앞 6프레임으로 뛰어오르고 뒤 2프레임으로 오른쪽 대각선 아래로 추락
SCENES = [
    {'name': 'idle', 'actor': 'a', 'frames': 'idle', 'frame_time': 0.12, 'duration': 2.64,
     'x': (START_X, START_X), 'direction': 1},
    {'name': 'walk right', 'actor': 'a', 'frames': 'walk', 'frame_time': 0.08, 'duration': 4.5,
     'x': (None, 1000), 'direction': 1},
    {'name': 'walk left', 'actor': 'a', 'frames': 'walk', 'frame_time': 0.08, 'duration': 3.5,
     'x': (None, 300), 'direction': -1},
    {'name': 'spin', 'actor': 'a', 'frames': 'spin', 'frame_time': 0.06, 'duration': 0.54,
     'x': (None, 460), 'direction': 1, 'once': True},
    {'name': 'roll', 'actor': 'a', 'frames': 'ball', 'frame_time': 0.06, 'duration': 1.44,
     'x': (None, 1000), 'direction': 1, 'bounces': [120, 120, 120, 120]},
    {'name': 'bounce back', 'actor': 'a', 'frames': 'ball', 'frame_time': 0.06, 'duration': 0.9,
     'x': (None, 700), 'direction': -1, 'bounces': [100, 60], 'ball_wait': True},
    {'name': 'far enter', 'actor': 'b', 'frames': 'dash', 'frame_time': 0.05, 'duration': 2.0,
     'x': (START_X, 550), 'y': (380, 260), 'scale': (1.5, 2.5), 'direction': 1},
    {'name': 'come near', 'actor': 'b', 'frames': 'peel_out', 'frame_time': 0.05, 'duration': 2.0,
     'x': (None, START_X), 'y': (None, GROUND_Y), 'scale': (None, SCALE), 'direction': -1},
    {'name': 'run kick', 'actor': 'b', 'frames': 'run', 'frame_time': 0.08, 'direction': 1,
     'kick': ('dash', 0.05), 'speed': 450, 'kick_frame': 4},
    {'name': 'leap', 'actor': 'b', 'frames': 'leap', 'frame_time': 0.12, 'duration': 1.72,
     'leap': (0.72, 1.0, 300, 150)},
    {'name': 'skid', 'actor': 'b', 'frames': 'skid', 'frame_time': 0.2, 'duration': 1.6,
     'x_path': [(800, 2), (450, 6)], 'direction': 1, 'once': True},
    {'name': 'hop', 'actor': 'b', 'frames': 'pose', 'frame_order': [0, 1], 'frame_time': 0.25,
     'duration': 0.5, 'direction': 1, 'once': True, 'bounces': [20]},
    {'name': 'pose', 'actor': 'b', 'frames': 'pose', 'frame_order': [2, 3, 2, 3], 'frame_time': 0.25,
     'duration': 1.0, 'direction': 1, 'once': True},
]


class Actor:
    # 화면에 그려지는 소닉 하나: 위치는 발(프레임 아래 변 중앙) 기준
    def __init__(self, x, y=GROUND_Y, scale=SCALE):
        self.frames = FRAMES['idle']
        self.frame_index = 0
        self.x, self.y = x, y
        self.height = 0             # 발 위치보다 위로 뜬 높이 (튕김, 점프)
        self.scale = scale
        self.direction = 1
        self.visible = False

    def draw(self):
        if self.visible:
            draw_frame(self.frames[self.frame_index], self.x, self.y + self.height,
                       self.direction, self.scale)


open_canvas(WIDTH, HEIGHT)

# 어느 폴더에서 실행해도 이 파일 옆의 이미지를 읽도록 경로를 만듦
sprite = load_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sonic-sprite.png'))
# 장면 이름 표시용 글꼴: pico2d 패키지에 들어 있는 글꼴 사용
font = load_font(os.path.join(os.path.dirname(pico2d.__file__), 'data', 'ConsolaMalgun.ttf'), 24)

running = True
sonic_a = Actor(START_X)
sonic_b = Actor(START_X)
actors = {'a': sonic_a, 'b': sonic_b}
scene_index = 0             # 지금 재생 중인 장면 번호
scene_time = 0.0            # 지금 장면이 시작된 뒤 지난 시간
finished = False            # 마지막 장면까지 끝났으면 True (마지막 화면 유지)
ball_state = 'scene'        # 공(소닉 A) 상태 - 'scene': 장면이 움직임, 'wait': 제자리에서 작게 튕김,
                            #                   'fly': 차여서 날아감, 'gone': 화면 밖으로 사라짐
ball_path = []              # 날아가는 공이 지나갈 점 [(x, 높이, 방향, 걸리는 시간), ...]
ball_from = (0, 0)          # 지금 구간을 시작한 공의 (x, 높이)
ball_time = 0.0             # 공이 지금 상태가 된 뒤 지난 시간
kick_stop = False           # 장면 9 에서 공 앞에 멈췄으면 True
kick_time = 0.0             # 멈춘 뒤 지난 시간
kicked = False              # 장면 9 에서 공을 찼으면 True


def handle_events():
    # 창의 X 버튼이나 ESC 키를 누르면 running 을 False 로 바꿔 종료
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw_frame(frame, x, y=GROUND_Y, direction=1, scale=SCALE):
    # frame = (left, bottom, w, h) 영역을 scale 배로 확대해 그림
    # 프레임마다 크기가 달라도 아래 변 중앙이 (x, y)에 오도록 중심 위치를 계산
    # 시트의 소닉은 오른쪽을 보므로 왼쪽(direction == -1)으로 갈 때는 좌우 반전
    left, bottom, w, h = frame
    if direction == 1:
        sprite.clip_draw(left, bottom, w, h, x, y + h * scale / 2, w * scale, h * scale)
    else:
        sprite.clip_composite_draw(left, bottom, w, h, 0, 'h', x, y + h * scale / 2, w * scale, h * scale)


def lerp(start, end, p):
    # start 에서 end 까지 p (0~1) 비율만큼 간 값
    return start + (end - start) * p


def bounce_height(t, duration, peaks):
    # 장면 시간 duration 을 튕김 수만큼 나눠, t 가 속한 튕김 안에서의 진행률 q 로 포물선 높이 계산
    # 4 * peak * q * (1 - q) 는 q = 0, 1 에서 0 (지면), q = 0.5 에서 peak
    section = duration / len(peaks)
    i = min(int(t / section), len(peaks) - 1)
    q = (t - i * section) / section
    return 4 * peaks[i] * q * (1 - q)


def start_scene(index):
    # index 번 장면 시작: 장면에 적힌 시작값으로 소닉을 맞추고, 없는 값은 앞 장면에서 이어받음
    global scene_index, scene_time
    scene_index = index
    scene_time = 0.0
    scene = SCENES[index]
    actor = actors[scene['actor']]
    actor.visible = True
    actor.frames = FRAMES[scene['frames']]
    if 'frame_order' in scene:
        actor.frames = [actor.frames[i] for i in scene['frame_order']]
    scene['start_x'] = actor.x
    actor.frame_index = 0
    actor.height = 0
    actor.direction = scene.get('direction', actor.direction)
    if actor.direction == 'auto':
        actor.direction = 1 if scene['x'][1] >= actor.x else -1
    # 보간할 값의 시작값이 None 이면 지금 값에서 시작
    scene['from'] = {}
    for key in ('x', 'y', 'scale'):
        if key in scene:
            start, end = scene[key]
            scene['from'][key] = getattr(actor, key) if start is None else start
            setattr(actor, key, scene['from'][key])   # 시작 화면부터 시작값으로 그려지도록


def next_scene():
    # 다음 장면으로, 마지막 장면이었으면 끝 (마지막 화면 유지)
    global finished
    if scene_index + 1 < len(SCENES):
        start_scene(scene_index + 1)
    else:
        finished = True


def frame_width(actor):
    # 지금 프레임을 확대해 그렸을 때의 가로 폭
    return actor.frames[actor.frame_index][2] * actor.scale


def update_kick(scene, actor, dt):
    # 달리는 줄 그림으로 공을 향해 달리다가, 차는 그림의 오른쪽 끝이 공 왼쪽 끝에 닿는 곳에서 멈춤
    # 멈춘 뒤 frames 줄을 한 번 재생하고, kick_frame 번째 그림이 나올 때 공을 참
    global kick_stop, kick_time, kicked
    kick_frames = FRAMES[scene['frames']]
    kick_half = kick_frames[scene['kick_frame']][2] * actor.scale / 2
    if not kick_stop:
        run_frames, run_time = scene['kick']
        actor.frames = FRAMES[run_frames]
        actor.frame_index = int(scene_time / run_time) % len(actor.frames)
        actor.x += scene['speed'] * dt
        ball_left = sonic_a.x - frame_width(sonic_a) / 2
        if actor.x + kick_half >= ball_left:
            kick_stop = True
            kick_time = 0.0
            actor.x = ball_left - kick_half     # 차는 순간 공과 딱 닿는 위치
            actor.frames = kick_frames
            actor.frame_index = 0
        return
    kick_time += dt
    actor.frame_index = min(int(kick_time / scene['frame_time']), len(actor.frames) - 1)
    if not kicked and actor.frame_index >= scene['kick_frame']:
        kicked = True
        start_ball_fly()


def update_leap(scene, actor, t):
    # 올라가는 동안: 1~6번 프레임, 처음엔 빠르고 끝에서 느려지게 top * (1 - (1-p)^2)
    # 떨어지는 동안: 7~8번 프레임을 0.1초씩 번갈아, 점점 빨라지게 top * (1 - p^2)
    # 떨어지는 동안 x 는 시작 위치에서 오른쪽으로 dx 만큼 이동 (오른쪽 대각선 아래)
    rise_time, fall_time, top, dx = scene['leap']
    if t < rise_time:
        p = t / rise_time
        actor.frame_index = min(int(t / scene['frame_time']), 5)
        actor.height = top * (1 - (1 - p) ** 2)
    else:
        p = min((t - rise_time) / fall_time, 1)
        actor.frame_index = 6 + int((t - rise_time) / 0.1) % 2
        actor.height = top * (1 - p ** 2)
        actor.x = scene['start_x'] + dx * p


def update_scene(dt):
    # 장면 경과 시간으로 프레임 번호와 위치, 크기를 계산
    global scene_time
    scene = SCENES[scene_index]
    actor = actors[scene['actor']]
    scene_time += dt
    if scene.get('kick'):
        update_kick(scene, actor, dt)
        if ball_state == 'gone':    # 찬 공이 화면 밖으로 사라지면 다음 장면
            next_scene()
        return
    t = min(scene_time, scene['duration'])
    p = t / scene['duration']
    for key in scene['from']:
        setattr(actor, key, lerp(scene['from'][key], scene[key][1], p))
    if 'bounces' in scene:
        actor.height = bounce_height(t, scene['duration'], scene['bounces'])
    if 'x_path' in scene:
        # 지금 시각 t 가 속한 구간을 찾아 그 구간 안에서 직선 이동
        x0, start = scene['start_x'], 0.0
        for x1, count in scene['x_path']:
            section = count * scene['frame_time']
            if t <= start + section:
                actor.x = lerp(x0, x1, (t - start) / section)
                break
            x0, start = x1, start + section
    # 장면 끝 순간에도 마지막 프레임을 보여주도록 끝 시각은 아주 조금 앞당겨 계산
    n = int(min(t, scene['duration'] - 1e-6) / scene['frame_time'])
    actor.frame_index = min(n, len(actor.frames) - 1) if scene.get('once') else n % len(actor.frames)
    if 'leap' in scene:
        update_leap(scene, actor, t)
    if scene_time >= scene['duration']:
        if scene.get('ball_wait'):
            start_ball_wait()
        next_scene()


def start_ball_wait():
    global ball_state, ball_time
    ball_state = 'wait'
    ball_time = 0.0


def start_ball_fly():
    # 공이 지나갈 점: 오른쪽 위 모서리(공 그림이 화면 오른쪽·위 끝에 닿는 곳)에서 튕긴 뒤
    # 반전해서 왼쪽 위 대각선으로, 소닉 B 머리 위 화면 밖까지
    global ball_state, ball_time, ball_path, ball_from
    w = sonic_a.frames[0][2] * sonic_a.scale
    h = sonic_a.frames[0][3] * sonic_a.scale
    corner = (WIDTH - w / 2, HEIGHT - h - sonic_a.y, 1, FLY_TO_CORNER)
    above_sonic = (sonic_b.x, HEIGHT - sonic_a.y + 10, -1, FLY_TO_TOP)
    ball_state = 'fly'
    ball_time = 0.0
    ball_path = [corner, above_sonic]
    ball_from = (sonic_a.x, sonic_a.height)
    sonic_a.direction = 1       # 처음에는 오른쪽으로 날아가므로 그림 방향도 오른쪽


def update_ball(dt):
    # 장면과 따로 공을 움직임
    # 기다리는 공은 프레임을 계속 돌리며 WAIT_PERIOD 마다 작게 튕김
    # 찬 공은 ball_path 의 점을 차례로 직선으로 날아가고, 마지막 점(화면 위 밖)에 닿으면 사라짐
    global ball_time, ball_state, ball_from
    if ball_state == 'wait':
        ball_time += dt
        sonic_a.frame_index = int(ball_time / BALL_FRAME_TIME) % len(sonic_a.frames)
        sonic_a.height = bounce_height(ball_time % WAIT_PERIOD, WAIT_PERIOD, [WAIT_BOUNCE])
    elif ball_state == 'fly':
        ball_time += dt
        sonic_a.frame_index = int(ball_time / BALL_FRAME_TIME) % len(sonic_a.frames)
        x, height, direction, duration = ball_path[0]
        p = min(ball_time / duration, 1)
        sonic_a.x = lerp(ball_from[0], x, p)
        sonic_a.height = lerp(ball_from[1], height, p)
        sonic_a.direction = direction
        if p >= 1:      # 이 점에 도착: 다음 점으로, 더 없으면 사라짐
            ball_path.pop(0)
            ball_from = (x, height)
            ball_time = 0.0
            if not ball_path:
                ball_state = 'gone'
                sonic_a.visible = False


def update(dt):
    if not finished:
        update_scene(dt)
    update_ball(dt)


def draw():
    clear_canvas()
    sonic_b.draw()
    sonic_a.draw()
    # 왼쪽 위에 지금 장면 번호와 이름 표시
    font.draw(20, HEIGHT - 30, '%d. %s' % (scene_index + 1, SCENES[scene_index]['name']), (0, 0, 0))
    update_canvas()


start_scene(0)
last_time = get_time()
while running:
    handle_events()
    now = get_time()
    update(now - last_time)
    last_time = now
    draw()
    delay(0.01)

close_canvas()
