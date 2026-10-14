#circle, triangle, star, quit을 
#한 줄씩 입력해 도형과 Wrong Shape 출력을 확인하세요.

import turtle

while True:
    shape=input("도형: ")

    if shape=='circle':
        turtle.circle(100)
    elif shape=='triangle':
        turtle.forward(100)
        turtle.left(120)
        turtle.forward(100)
        turtle.left(120)
        turtle.forward(100)
    elif shape=='star':
        count=5
        while count>0:
            turtle.forward(100)
            turtle.left(144)
            count-=1
    elif shape=='quit':
        break
    else:
        print("Wrong Shape")
