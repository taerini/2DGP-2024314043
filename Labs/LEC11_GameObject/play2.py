from pico2d import *
import random

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


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
        self.run_image = load_image('run_animation.png')       # 혼자 달릴 때
        self.sheet_image = load_image('animation_sheet.png')   # 조종될 때

        # 조종 관련 값
        self.controlled = False     # 지금 조종되고 있는지
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 5
        self.facing = 1
        self.state = 'idle_right'

        # 조종될 때 쓰는 동작: (시트에서 줄 위치, 프레임 수)
        self.animations = {
            'run_right':  (100, 8),
            'run_left':   (0,   8),
            'idle_right': (300, 8),
            'idle_left':  (200, 8),
        }

    def update(self):
        if self.controlled == True:
            self.update_controlled()
        else:
            self.update_auto()

    def update_auto(self):
        # 혼자 오른쪽으로 달리기
        self.frame = self.frame + 1
        if self.frame >= 8:
            self.frame = 0

        self.x = self.x + 5

        # 오른쪽 끝을 넘어가면 왼쪽에서 다시 나오기
        if self.x > CANVAS_WIDTH + 50:
            self.x = -50

    def update_controlled(self):
        # 1. 위치 이동
        self.x = self.x + self.dir_x * self.speed
        self.y = self.y + self.dir_y * self.speed

        # 2. 바라보는 방향 기억
        if self.dir_x != 0:
            self.facing = self.dir_x

        # 3. 움직이는 중인지 확인
        if self.dir_x != 0 or self.dir_y != 0:
            moving = True
        else:
            moving = False

        # 4. 방향 이름
        if self.facing == 1:
            side = 'right'
        else:
            side = 'left'

        # 5. 상태 이름
        if moving == True:
            new_state = 'run_' + side
        else:
            new_state = 'idle_' + side

        # 6. 동작이 바뀌면 프레임 처음부터
        if new_state != self.state:
            self.state = new_state
            self.frame = 0

        # 7. 다음 프레임
        animation = self.animations[self.state]
        frame_count = animation[1]
        self.frame = self.frame + 1
        if self.frame >= frame_count:
            self.frame = 0

    def draw(self):
        if self.controlled == True:
            animation = self.animations[self.state]
            row = animation[0]
            self.sheet_image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
        else:
            self.run_image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def is_clicked(self, mouse_x, mouse_y):
        # 소년 그림 박스(100x100) 안을 클릭했는지 확인
        left = self.x - 50
        right = self.x + 50
        bottom = self.y - 50
        top = self.y + 50

        if mouse_x >= left and mouse_x <= right and mouse_y >= bottom and mouse_y <= top:
            return True
        else:
            return False

    def start_control(self):
        self.controlled = True
        self.dir_x = 0
        self.dir_y = 0
        self.facing = 1
        self.state = 'idle_right'
        self.frame = 0

    def stop_control(self):
        self.controlled = False
        self.y = 90                 # 다시 잔디 위로
        self.frame = 0


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

        if self.x > CANVAS_WIDTH + 100:
            self.x = -100

    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h

        self.image.clip_draw(
            self.frame * frame_width, 0,
            frame_width, frame_height,
            self.x, self.y,
            frame_width // 2, frame_height // 2
        )


# ===== 이벤트 처리 =====

def handle_events():
    global running
    global selected

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False

        # 마우스 클릭: 소년 고르기
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x = event.x
            mouse_y = CANVAS_HEIGHT - 1 - event.y     # 마우스 좌표 → pico2d 좌표

            for boy in team:
                if boy.is_clicked(mouse_x, mouse_y) == True:
                    if selected != None:
                        selected.stop_control()       # 원래 조종하던 소년은 놓아주기
                    selected = boy
                    selected.start_control()          # 새 소년 조종 시작
                    break                             # 한 명 찾았으면 그만 찾기

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

            if selected != None:
                if event.key == SDLK_RIGHT:
                    selected.dir_x = selected.dir_x + 1
                elif event.key == SDLK_LEFT:
                    selected.dir_x = selected.dir_x - 1
                elif event.key == SDLK_UP:
                    selected.dir_y = selected.dir_y + 1
                elif event.key == SDLK_DOWN:
                    selected.dir_y = selected.dir_y - 1

        elif event.type == SDL_KEYUP:
            if selected != None:
                if event.key == SDLK_RIGHT:
                    selected.dir_x = selected.dir_x - 1
                elif event.key == SDLK_LEFT:
                    selected.dir_x = selected.dir_x + 1
                elif event.key == SDLK_UP:
                    selected.dir_y = selected.dir_y - 1
                elif event.key == SDLK_DOWN:
                    selected.dir_y = selected.dir_y + 1


# ===== 게임 월드 =====

def reset_world():
    global running
    global world
    global team
    global selected

    running = True
    world = []
    team = []           # 클릭 확인용으로 소년들만 따로 모아둠
    selected = None     # 아직 아무도 조종하지 않음

    grass = Grass()
    world.append(grass)

    for i in range(11):
        boy = Boy()
        world.append(boy)
        team.append(boy)

    zombie = Zombie()
    world.append(zombie)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


# ===== 실행 부분 =====

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()