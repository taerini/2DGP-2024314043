from pico2d import *
import json

WIDTH, HEIGHT = 800, 600
CENTER_X = WIDTH // 2      # 캐릭터를 그릴 가로 중앙
GROUND_Y = 120             # 캐릭터 발이 닿는 높이
SCALE = 6                  # 확대 배율 (키 55px -> 330px, 화면 높이의 절반 이상)
FRAME_TIME = 0.1           # 프레임 하나를 보여주는 시간(초)
REPEAT = 5                 # 애니메이션 하나를 반복하는 횟수
PAUSE_TIME = 1.0           # 반복이 끝난 뒤 정지하는 시간(초)

open_canvas(WIDTH, HEIGHT)

sprite = load_image('sprite_sheet.png')
with open('sprite_sheet.json') as f:
    frames = json.load(f)['animations']   # 애니메이션 이름 -> 프레임(x, y, w, h, ax, ay) 목록


def draw_frame(frame):
    # 시트에서 frame 영역만 잘라서 SCALE 배로 확대해 화면에 그림
    # 프레임마다 크기가 달라도 발 기준점(ax, ay)이 항상 (CENTER_X, GROUND_Y)에 오도록 왼쪽 아래 위치를 계산
    left = CENTER_X - frame['ax'] * SCALE
    bottom = GROUND_Y - frame['ay'] * SCALE
    sprite.clip_draw_to_origin(frame['x'], frame['y'], frame['w'], frame['h'],
                               left, bottom, frame['w'] * SCALE, frame['h'] * SCALE)


def play_animation(name):
    # name 애니메이션을 REPEAT 회 반복 재생한 뒤 PAUSE_TIME 동안 정지
    # 프레임 목록을 그대로 돌기 때문에 애니메이션마다 프레임 수가 달라도 동작
    for _ in range(REPEAT):
        for frame in frames[name]:
            clear_canvas()
            draw_frame(frame)
            update_canvas()
            delay(FRAME_TIME)
    delay(PAUSE_TIME)


def draw_idle():
    play_animation('idle')

def draw_walk():
    play_animation('walk')

def draw_run():
    play_animation('run')

def draw_jump():
    play_animation('jump')

def draw_attack():
    pass


while True:
    draw_idle()
    draw_walk()
    draw_run()
    draw_jump()
    draw_attack()


close_canvas()
