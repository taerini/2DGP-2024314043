from pico2d import *
import json

open_canvas()

sprite = load_image('sprite_sheet.png')
with open('sprite_sheet.json') as f:
    frames = json.load(f)['animations']   # 애니메이션 이름 -> 프레임(x, y, w, h, ax, ay) 목록


close_canvas()
