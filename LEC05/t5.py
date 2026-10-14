from pico2d import *

canvas_width = 800
canvas_height = 600
open_canvas(canvas_width, canvas_height)

running = True

boy = load_image('character.png')

x = 400       # 가로 위치
y = 300       # 세로 위치
dir_x = 0     # 좌우 방향: -1(왼쪽), 0, 1(오른쪽)
dir_y = 0     # 상하 방향: -1(아래), 0, 1(위)


def update():
    global x, y
    x += dir_x * 5
    y += dir_y * 5
    return x, y


def draw(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.02)


def handle_events():
    global running
    global dir_x, dir_y

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1


while running:
    handle_events()
    x, y = update()
    draw(x, y)

close_canvas()