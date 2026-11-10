from pico2d import *
import game_world
import game_framework
import title_mode
import pause_mode
import item_mode
from boy import Boy
from grass import Grass


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_mode(pause_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(item_mode)
        else:
            boy.handle_event(event)



def init():
    global boy


    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)



def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    global paused_at
    paused_at = get_time()

def resume():
    # 정지했던 시간만큼 미뤄서, 다시 시작하자마자 소년이 잠들지 않게 함
    boy.idle_started_at += get_time() - paused_at
    # 다른 모드에 있는 동안 뗀 방향키는 전달되지 않으므로 키 상태를 초기화
    boy.pressed_keys.clear()
    if boy.state == 'RUN':
        boy.dir = 0
        boy.stop_run()


running = True

