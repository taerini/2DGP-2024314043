from pico2d import *
import math

open_canvas(800, 600)

character = load_image('character.png')
grass = load_image('grass.png')


center_x, center_y = 400, 300   
radius = 150                   
angle = 0                     
angle_speed = 2               

while True:
    clear_canvas()
    grass.draw(400, 30)


    rad = math.radians(angle)
    x = center_x + radius * math.cos(rad)
    y = center_y + radius * math.sin(rad)



    character.draw(x, y)
    update_canvas()

    angle += angle_speed
    angle %= 360  

    delay(0.02)

close_canvas()