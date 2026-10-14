from pico2d import *        # pico2d의 모든 기능(open_canvas, load_image 등)을 이름만으로 쓸 수 있게 가져옴
import math                 # 수학 함수(sin, cos, radians)를 쓰려고 math 모듈을 가져옴

open_canvas(800, 600)       # 가로 800, 세로 600 크기의 창을 엶 (이미지 불러오기보다 먼저 해야 함)

character = load_image('character.png')   # 캐릭터 이미지를 불러와 character에 저장
grass = load_image('grass.png')           # 잔디 이미지를 불러와 grass에 저장


center_x, center_y = 400, 300   # 원의 중심 좌표 (화면 한가운데). 여러 변수 동시 대입
radius = 150                    # 원의 반지름: 중심에서 150픽셀 떨어진 곳을 돎
angle = 0                       # 현재 각도 (0도 = 중심의 오른쪽에서 출발)
angle_speed = 2                 # 한 프레임마다 각도를 2도씩 늘림 → 숫자가 클수록 빨리 돎

while True:                     # 무한 반복 (매 반복이 화면 한 장 = 한 프레임)
    clear_canvas()              # 이전 프레임의 그림을 지움 (안 지우면 잔상이 남음)
    grass.draw(400, 30)         # 잔디를 화면 아래쪽 (400, 30)에 그림


    rad = math.radians(angle)   # 각도(도)를 라디안으로 바꿈. sin, cos는 라디안 단위만 받음
    x = center_x + radius * math.cos(rad)   # 원 위의 x좌표 = 중심 x + 반지름 × cos(각도)
    y = center_y + radius * math.sin(rad)   # 원 위의 y좌표 = 중심 y + 반지름 × sin(각도)



    character.draw(x, y)        # 계산한 (x, y) 위치에 캐릭터를 그림
    update_canvas()             # 지금까지 그린 것을 실제 화면에 보여 줌

    angle += angle_speed        # 각도를 2도 늘림 → 다음 프레임에는 조금 더 돈 위치
    angle %= 360                # 360으로 나눈 나머지 → 360도가 되면 다시 0도로 (각도가 무한히 커지지 않게)

    delay(0.02)                 # 0.02초 멈춤 → 너무 빨리 돌지 않게 속도 조절

close_canvas()                  # 창을 닫음 (while True가 끝나지 않아서 실제로는 실행되지 않음)
