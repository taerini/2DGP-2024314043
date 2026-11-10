from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    image = None

    def __init__(self, x, y, velocity):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.velocity = velocity

    def update(self):
        self.x += self.velocity
        # 화면 밖으로 나가면 게임 월드에서 스스로 제거된다
        if self.x < -10 or self.x > get_canvas_width() + 10:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
