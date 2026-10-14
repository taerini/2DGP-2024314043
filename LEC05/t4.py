from pico2d import*

open_canvas()
character=load_image('character.png')

def circle():
    for speed in range(360):
        rad=math.radiant(speed)
        x=400+400*math.cos(rad)
        y=300+400*math.sin(rad)

        clear_canvas()
        character.draw(x,y)
        update_canvas()
        delay(0.01)



while True:
    circle()


close_canvas()