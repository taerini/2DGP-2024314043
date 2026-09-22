from pico2d import*
  

open_canvas(800, 600)

character = load_image('character.png')
grass = load_image('grass.png')

r=4
while r>=0:
    x=200
    while x<600:
        clear_canvas()
        grass.draw(400,30)
        character.draw(x, 90)
        update_canvas()
        x+=2
        delay(0.01)

    y=90
    while y<490:
        clear_canvas()
        grass.draw(400,30)
        character.draw(600, y)
        update_canvas()
        y+=2
        delay(0.01)

    x2=600
    while x2>200:
        clear_canvas()
        grass.draw(400,30)
        character.draw(x2,490)
        update_canvas()
        x2-=2
        delay(0.01)

    y2=490
    while y2>90:
        clear_canvas()
        grass.draw(400,30)
        character.draw(200, y2)
        update_canvas()
        y2-=2
        delay(0.01)
    r-=1


close_canvas()







