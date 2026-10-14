from pico2d import*

open_canvas(800, 600)

boy=load_image('animation_sheet.png')
grass=load_image('grass.png')


frame=0

for x in range(0, 800, 5):
    clear_canvas()
    grass.draw(400,30)
    boy.clip_composite_draw (
        frame*100, 0, 
        100, 100,
        0, 'h',
        x, 90,
        200,200
    )

    update_canvas()

    frame=(frame+1)%8
    delay(0.05)

close_canvas()

