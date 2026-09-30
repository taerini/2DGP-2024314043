from pico2d import *
import json

WIDTH, HEIGHT = 800, 600
CENTER_X = WIDTH // 2      # 캐릭터를 그릴 가로 중앙
GROUND_Y = 120             # 캐릭터 발이 닿는 높이

open_canvas(WIDTH, HEIGHT)

sprite = load_image('sprite_sheet.png')
with open('sprite_sheet.json') as f:
    frames = json.load(f)['animations']   # 애니메이션 이름 -> 프레임(x, y, w, h, ax, ay) 목록


def draw_idle():
    pass

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
