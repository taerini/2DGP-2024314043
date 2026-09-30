from pico2d import *
import json

WIDTH, HEIGHT = 800, 600
CENTER_X = WIDTH // 2      # 캐릭터를 그릴 가로 중앙
GROUND_Y = 120             # 캐릭터 발이 닿는 높이
SCALE = 6                  # 확대 배율 (키 55px -> 330px, 화면 높이의 절반 이상)

open_canvas(WIDTH, HEIGHT)

sprite = load_image('sprite_sheet.png')
with open('sprite_sheet.json') as f:
    frames = json.load(f)['animations']   # 애니메이션 이름 -> 프레임(x, y, w, h, ax, ay) 목록


def draw_frame(frame):
    # 시트에서 frame 영역만 잘라서 SCALE 배로 확대해 화면에 그림
    sprite.clip_draw(frame['x'], frame['y'], frame['w'], frame['h'],
                     CENTER_X, GROUND_Y, frame['w'] * SCALE, frame['h'] * SCALE)


def draw_idle():
    clear_canvas()
    draw_frame(frames['idle'][0])
    update_canvas()

def draw_walk():
    pass

def draw_run():
    pass

def draw_jump():
    pass

def draw_attack():
    pass


while True:
    draw_idle()
    draw_walk()
    draw_run()
    draw_jump()
    draw_attack()


close_canvas()
