from pico2d import *


# fill here

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground= load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')


def handle_events():
    global running
    global x, y

    # fill here

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, TUK_HEIGHT - 1 - event.y
        elif event
        # fill here


running = True
frame = 0

# fill here



while running:
    clear_canvas()

    # fill here

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    delay(0.05)

close_canvas()




