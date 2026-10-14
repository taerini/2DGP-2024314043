from pico2d import *
import random


# ===== 게임 오브젝트 클래스 =====

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)


class Boy:
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = 90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = self.frame + 1
        if self.frame >= 8:
            self.frame = 0

        self.x = self.x + 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


class Zombie:
    def __init__(self):
        self.x = 100
        self.y = 170
        self.frame = 0
        self.image = load_image('zombie_run_animation.png')

    def update(self):
        self.frame = self.frame + 1
        if self.frame >= 10:
            self.frame = 0

        self.x = self.x + 5

    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h

        self.image.clip_draw(
            self.frame * frame_width, 0,
            frame_width, frame_height,
            self.x, self.y,
            frame_width // 2, frame_height // 2
        )


class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.dir_x = 0              # 좌우 방향: -1(왼쪽), 0(정지), 1(오른쪽)
        self.dir_y = 0              # 상하 방향: -1(아래), 0(정지), 1(위)
        self.speed = 5
        self.frame = 0
        self.facing = 1             # 마지막으로 바라본 방향: 1(오른쪽), -1(왼쪽)
        self.state = 'idle_right'
        self.image = load_image('animation_sheet.png')

        # 동작 이름: (시트에서 줄 위치, 프레임 수)
        self.animations = {
            'run_right':  (100, 8),
            'run_left':   (0,   8),
            'idle_right': (300, 8),
            'idle_left':  (200, 8),
        }

    def update(self):
        # 1. 위치 이동
        self.x = self.x + self.dir_x * self.speed
        self.y = self.y + self.dir_y * self.speed

        # 2. 좌우로 움직이고 있으면 바라보는 방향 기억
        if self.dir_x != 0:
            self.facing = self.dir_x

        # 3. 움직이는 중인지 확인
        if self.dir_x != 0 or self.dir_y != 0:
            moving = True
        else:
            moving = False

        # 4. 바라보는 방향 이름 정하기
        if self.facing == 1:
            side = 'right'
        else:
            side = 'left'

        # 5. 상태 이름 정하기
        if moving == True:
            new_state = 'run_' + side
        else:
            new_state = 'idle_' + side

        # 6. 동작이 바뀌었으면 프레임을 처음부터
        if new_state != self.state:
            self.state = new_state
            self.frame = 0

        # 7. 다음 프레임으로 넘기기
        animation = self.animations[self.state]
        frame_count = animation[1]
        self.frame = self.frame + 1
        if self.frame >= frame_count:
            self.frame = 0

    def draw(self):
        animation = self.animations[self.state]
        row = animation[0]
        self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)


# ===== 이벤트 처리 =====

def handle_events():
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                player.dir_x = player.dir_x + 1
            elif event.key == SDLK_LEFT:
                player.dir_x = player.dir_x - 1
            elif event.key == SDLK_UP:
                player.dir_y = player.dir_y + 1
            elif event.key == SDLK_DOWN:
                player.dir_y = player.dir_y - 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.dir_x = player.dir_x - 1
            elif event.key == SDLK_LEFT:
                player.dir_x = player.dir_x + 1
            elif event.key == SDLK_UP:
                player.dir_y = player.dir_y - 1
            elif event.key == SDLK_DOWN:
                player.dir_y = player.dir_y + 1


# ===== 게임 월드 =====

def reset_world():
    global running
    global world
    global player

    running = True
    world = []

    # 잔디 (맨 먼저 넣어야 맨 뒤에 그려짐)
    grass = Grass()
    world.append(grass)

    # 소년 11명
    for i in range(11):
        boy = Boy()
        world.append(boy)

    # 좀비
    zombie = Zombie()
    world.append(zombie)

    # 플레이어 (맨 마지막에 넣어야 맨 위에 그려짐)
    player = Player()
    world.append(player)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


# ===== 실행 부분 =====

open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()