class Idle:
    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.frame = 0

    def exit(self):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)


class StateMachine:
    def __init__(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()
