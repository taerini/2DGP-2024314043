from pico2d import*

open_canvas(800, 600)

grass=load_image('grass.png')
character=load_image('character.png')


def move_character(character_recent, x,y):
    for i in range(0,40):
        clear_canvas()
        character_recent=(character_recent[0]+x, character_recent[1]+y)
        grass.draw(400,30)
        character.draw(character_recent[0], character_recent[1])
        update_canvas()
        delay(0.03)
    return character_recent



character_recent=(200,60)
grass.draw(400, 30)
character.draw(character_recent[0], character_recent[1])



while True:
    character_recent = move_character(character_recent, 10, 0)
    character_recent = move_character(character_recent, 0, 10)
    character_recent = move_character(character_recent, -10, 0)
    character_recent = move_character(character_recent, 0, -10)

close_canvas()
