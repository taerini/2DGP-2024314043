import turtle

def rectangle_area(width, height):
    return width*height


for i in range(2):
    width=int(input("가로: "))
    height=int(input("세로: "))
    print(rectangle_area(width, height))
    