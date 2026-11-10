from pico2d import *
from boy import Boy
from grass import Grass

import game_world #게임 월드 모듈 임포트


# Game object class here


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)



def reset_world():
    global boy
    
    boy = Boy()
    game_world.add_object(boy, 1) #레이어 1에 소년 객체 추가
    

    grass = Grass()
    game_world.add_object(grass, 0) #레이어 0에 잔디 객체 추가

   


def update_world():
    game_world.update() #게임 월드의 모든 객체를 업데이트
    pass


def render_world():
    clear_canvas()
    game_world.render() #게임 월드의 모든 객체를 렌더링
    update_canvas()


running = True



open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()

