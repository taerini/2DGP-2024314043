import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 이미지 경로 기준을 이 폴더로

import game_framework
from pico2d import *
import logo_mode
import title_mode
import play_mode

open_canvas()
game_framework.run(logo_mode)
close_canvas()
