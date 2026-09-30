from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png ')

# fill here
frame=0




def draw_walk():
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, 400, 90)
    update_canvas()
    pass

def draw_run_left():
    for x in range(0, 800, 5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_composite_draw(
            frame*100, 0,   #left, bottom
            100, 100,  #width, height
                x, 90,   #x, y
                )
        update_canvas()

    frame=(frame+1)%8
    delay(0.05)
    pass

def draw_jump():
    pass

def draw_attack():
    pass



while True:
    draw_walk()
    draw_run_left()
    draw_jump()
    draw_attack()


close_canvas()

