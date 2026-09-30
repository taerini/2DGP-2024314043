# sprite_sheet.png / sprite_sheet.json 생성기 (외부 라이브러리 없이 순수 파이썬)
#
# - 애니메이션 5종: idle(4), walk(6), run(8), jump(5), attack(7) -> 애니메이션별 프레임 수가 모두 다름
# - 각 프레임은 그림이 있는 영역만큼 잘라서 배치 -> 프레임마다 크기가 다름
# - 프레임 위치/크기/기준점은 sprite_sheet.json 에 저장 (y 는 pico2d 처럼 아래쪽 기준)

import json
import math
import struct
import zlib

CANVAS = 160          # 프레임 하나를 그릴 임시 캔버스 크기
ORIGIN_X = 70         # 캔버스 안에서 발 기준점 x
GROUND_Y = 20         # 캔버스 안에서 땅 높이

THIGH, SHIN = 10, 10
TORSO = 14
UPPER_ARM, FOREARM = 8, 8
HEAD_R = 7
SWORD = 20

OUTLINE = (20, 20, 30, 255)
SKIN = (255, 205, 160, 255)
SKIN_BACK = (225, 175, 135, 255)
HAIR = (70, 45, 30, 255)
SHIRT = (60, 120, 220, 255)
SHIRT_BACK = (45, 90, 170, 255)
PANTS = (55, 55, 90, 255)
PANTS_BACK = (40, 40, 65, 255)
SHOE = (40, 30, 30, 255)
BLADE = (215, 225, 235, 255)
HILT = (160, 110, 40, 255)
SLASH = (255, 250, 190, 170)


def direction(angle):
    """아래쪽을 0도로, 앞(+x)쪽으로 도는 각도를 단위 벡터로"""
    a = math.radians(angle)
    return math.sin(a), -math.cos(a)


def add(p, d, length):
    return p[0] + d[0] * length, p[1] + d[1] * length


class Canvas:
    def __init__(self):
        self.px = [[(0, 0, 0, 0)] * CANVAS for _ in range(CANVAS)]  # [y][x], y 는 위쪽이 +

    def capsule(self, p1, p2, r, color):
        x0 = int(min(p1[0], p2[0]) - r - 1)
        x1 = int(max(p1[0], p2[0]) + r + 1)
        y0 = int(min(p1[1], p2[1]) - r - 1)
        y1 = int(max(p1[1], p2[1]) + r + 1)
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        seg = dx * dx + dy * dy
        for y in range(max(0, y0), min(CANVAS, y1 + 1)):
            for x in range(max(0, x0), min(CANVAS, x1 + 1)):
                cx, cy = x + 0.5, y + 0.5
                t = 0 if seg == 0 else max(0, min(1, ((cx - p1[0]) * dx + (cy - p1[1]) * dy) / seg))
                ex, ey = p1[0] + dx * t - cx, p1[1] + dy * t - cy
                if ex * ex + ey * ey <= r * r:
                    self.px[y][x] = color

    def part(self, p1, p2, r, color):
        """외곽선을 먼저 칠하고 안쪽을 칠해서 부위마다 테두리가 생기게"""
        self.capsule(p1, p2, r + 1, OUTLINE)
        self.capsule(p1, p2, r, color)

    def arc(self, center, radius, a_from, a_to, width):
        lo, hi = min(a_from, a_to), max(a_from, a_to)
        for y in range(CANVAS):
            for x in range(CANVAS):
                if self.px[y][x][3]:
                    continue  # 캐릭터 뒤쪽에만 궤적을 그림
                vx, vy = x + 0.5 - center[0], y + 0.5 - center[1]
                d = math.hypot(vx, vy)
                if not radius - width <= d <= radius:
                    continue
                a = math.degrees(math.atan2(vx, -vy))
                if a < lo - 180:
                    a += 360
                if lo <= a <= hi:
                    self.px[y][x] = SLASH

    def crop(self):
        xs = [x for y in range(CANVAS) for x in range(CANVAS) if self.px[y][x][3]]
        ys = [y for y in range(CANVAS) for x in range(CANVAS) if self.px[y][x][3]]
        x0, x1, y0, y1 = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
        rows = [self.px[y][x0:x1 + 1] for y in range(y0, y1 + 1)]
        # 기준점(발이 땅에 닿는 점)을 잘라낸 프레임의 왼쪽 아래 기준으로
        return rows, ORIGIN_X - x0, GROUND_Y - y0


def leg_points(hip, thigh, knee):
    k = add(hip, direction(thigh), THIGH)
    return k, add(k, direction(thigh + knee), SHIN)


def arm_points(shoulder, upper, elbow):
    e = add(shoulder, direction(upper), UPPER_ARM)
    return e, add(e, direction(upper + elbow), FOREARM)


def draw_pose(pose):
    """pose: lean, air, legs=[뒤,앞](허벅지각, 무릎각), arms=[뒤,앞](어깨각, 팔꿈치각), sword, slash"""
    c = Canvas()

    # 가장 낮은 발이 땅에 닿도록 엉덩이 높이를 정함
    feet = [leg_points((0, 0), *leg)[1] for leg in pose['legs']]
    hip = (ORIGIN_X, GROUND_Y + 3 - min(f[1] for f in feet) + pose.get('air', 0))

    lean = math.radians(pose.get('lean', 0))
    up = (math.sin(lean), math.cos(lean))
    shoulder = add(hip, up, TORSO)
    head = add(shoulder, up, HEAD_R + 1)

    (back_leg, front_leg), (back_arm, front_arm) = pose['legs'], pose['arms']

    # 뒤쪽 팔/다리
    e, h = arm_points(shoulder, *back_arm)
    c.part(shoulder, e, 2, SHIRT_BACK)
    c.part(e, h, 1.5, SKIN_BACK)
    k, f = leg_points(hip, *back_leg)
    c.part(hip, k, 2.5, PANTS_BACK)
    c.part(k, f, 2, PANTS_BACK)
    c.part(f, (f[0] + 2, f[1]), 2, SHOE)

    # 몸통, 머리
    c.part(hip, shoulder, 4, SHIRT)
    c.part(head, head, HEAD_R, SKIN)
    for y in range(int(head[1] - HEAD_R), int(head[1] + HEAD_R) + 1):
        for x in range(int(head[0] - HEAD_R), int(head[0] + HEAD_R) + 1):
            dx, dy = x + 0.5 - head[0], y + 0.5 - head[1]
            if dx * dx + dy * dy <= HEAD_R * HEAD_R and (dy > 1 or dx < -3):
                c.px[y][x] = HAIR
    c.px[int(head[1])][int(head[0] + 3)] = OUTLINE  # 눈

    # 앞쪽 다리
    k, f = leg_points(hip, *front_leg)
    c.part(hip, k, 2.5, PANTS)
    c.part(k, f, 2, PANTS)
    c.part(f, (f[0] + 2, f[1]), 2, SHOE)

    # 앞쪽 팔 (+ 칼)
    e, h = arm_points(shoulder, *front_arm)
    if pose.get('sword'):
        d = direction(front_arm[0] + front_arm[1])
        guard = (-d[1] * 3, d[0] * 3)
        c.part(add(h, d, 2), add(h, d, SWORD), 1, BLADE)
        c.part((h[0] + guard[0], h[1] + guard[1]), (h[0] - guard[0], h[1] - guard[1]), 1, HILT)
    c.part(shoulder, e, 2, SHIRT)
    c.part(e, h, 1.5, SKIN)

    if pose.get('slash'):
        a_from, a_to = pose['slash']
        c.arc(shoulder, UPPER_ARM + FOREARM + SWORD, a_from, a_to, 5)

    return c.crop()


def idle_poses():
    poses = []
    for bend in (0, 14, 28, 14):
        poses.append(dict(lean=0,
                          legs=[(-5 + bend, -2 * bend), (5 + bend, -2 * bend)],
                          arms=[(-8, 10 + bend), (8, 10 + bend)]))
    return poses


def walk_poses():
    poses = []
    for i in range(6):
        p = 2 * math.pi * i / 6
        s = math.sin(p)
        poses.append(dict(lean=3,
                          legs=[(-25 * s, -(5 + 30 * max(0, s))), (25 * s, -(5 + 30 * max(0, -s)))],
                          arms=[(20 * s, 15), (-20 * s, 15)]))
    return poses


def run_poses():
    poses = []
    for i in range(8):
        p = 2 * math.pi * i / 8
        s, co = math.sin(p), math.cos(p)
        poses.append(dict(lean=15, air=3 * abs(co),
                          legs=[(-45 * s, -(25 + 60 * (0.5 - 0.5 * co))),
                                (45 * s, -(25 + 60 * (0.5 + 0.5 * co)))],
                          arms=[(50 * s, 80), (-50 * s, 80)]))
    return poses


def jump_poses():
    return [
        dict(lean=20, air=0, legs=[(50, -90), (60, -95)], arms=[(-40, 20), (-30, 20)]),     # 웅크리기
        dict(lean=5, air=14, legs=[(-10, -5), (0, -10)], arms=[(160, 10), (170, 10)]),      # 도약
        dict(lean=0, air=32, legs=[(70, -110), (80, -100)], arms=[(120, 30), (130, 30)]),   # 최고점
        dict(lean=-5, air=18, legs=[(10, -30), (25, -20)], arms=[(70, 20), (80, 20)]),      # 낙하
        dict(lean=25, air=0, legs=[(55, -100), (65, -100)], arms=[(30, 30), (40, 30)]),     # 착지
    ]


def attack_poses():
    stance = [(-20, 0), (25, -20)]
    lunge = [(-30, 0), (45, -45)]
    return [
        dict(lean=0, legs=stance, arms=[(-20, 30), (30, 60)], sword=True),                    # 준비
        dict(lean=-8, legs=stance, arms=[(-30, 30), (200, 20)], sword=True),                  # 들어올리기
        dict(lean=-12, legs=stance, arms=[(-35, 30), (215, 10)], sword=True),                 # 최대 준비
        dict(lean=5, legs=lunge, arms=[(-40, 30), (130, 0)], sword=True, slash=(130, 215)),   # 휘두르기
        dict(lean=15, legs=lunge, arms=[(-45, 30), (75, 0)], sword=True, slash=(75, 215)),    # 타격
        dict(lean=20, legs=lunge, arms=[(-45, 30), (35, 0)], sword=True, slash=(35, 130)),    # 마무리
        dict(lean=5, legs=stance, arms=[(-25, 30), (30, 45)], sword=True),                    # 복귀
    ]


ANIMATIONS = [
    ('idle', idle_poses),
    ('walk', walk_poses),
    ('run', run_poses),
    ('jump', jump_poses),
    ('attack', attack_poses),
]
GAP = 2


def write_png(path, rows):
    """rows: 위쪽 줄부터 순서대로, 픽셀은 (r, g, b, a)"""
    h, w = len(rows), len(rows[0])
    raw = b''.join(b'\x00' + bytes(v for p in row for v in p) for row in rows)

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data))

    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(raw, 9)))
        f.write(chunk(b'IEND', b''))


def main():
    # 애니메이션 하나를 한 줄로, 줄 안에서는 왼쪽부터 아래쪽 정렬로 배치
    lines = []
    for name, make in ANIMATIONS:
        lines.append((name, [draw_pose(p) for p in make()]))

    sheet_w = max(sum(len(rows[0]) + GAP for rows, _, _ in frames) for _, frames in lines) + GAP
    sheet_h = sum(max(len(rows) for rows, _, _ in frames) + GAP for _, frames in lines) + GAP
    sheet = [[(0, 0, 0, 0)] * sheet_w for _ in range(sheet_h)]  # [y][x], y 는 위쪽이 +

    meta = {'image': 'sprite_sheet.png', 'animations': {}}
    bottom = sheet_h - GAP
    for name, frames in lines:
        line_h = max(len(rows) for rows, _, _ in frames)
        bottom -= line_h
        x = GAP
        meta['animations'][name] = []
        for rows, ax, ay in frames:
            fh, fw = len(rows), len(rows[0])
            for y in range(fh):
                sheet[bottom + y][x:x + fw] = rows[y]
            meta['animations'][name].append(dict(x=x, y=bottom, w=fw, h=fh, ax=ax, ay=ay))
            x += fw + GAP
        bottom -= GAP

    write_png('sprite_sheet.png', sheet[::-1])
    with open('sprite_sheet.json', 'w') as f:
        json.dump(meta, f, indent=2)

    for name, frames in meta['animations'].items():
        sizes = ', '.join(f"{fr['w']}x{fr['h']}" for fr in frames)
        print(f'{name:7} {len(frames)} frames: {sizes}')


if __name__ == '__main__':
    main()
