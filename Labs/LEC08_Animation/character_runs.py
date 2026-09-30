from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

# fill here
frame=0

for x in range(800, 0, 5):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_composite_draw(
        frame*100, 0,   #left, bottom
          100, 100,  #width, height
         # math.pi/2, 'h', #rotation, scale
            x, 90,   #x, y
              200, 200  #width, height
            )
    update_canvas()

    frame=(frame+1)%8
    delay(0.05)

close_canvas()

