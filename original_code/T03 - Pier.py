# t03-boustrophedon-assn.py

import turtle
# main
def main():
    wn = turtle.Screen()
    wn.setup(width=600, height=600)
    wn.bgcolor("black")
    alex = turtle.Turtle()
    tess = turtle.Turtle()
    alex.color("purple")
    alex.speed(100)
    alex.penup()
    alex.setpos(-280,-280)
    alex.pendown()
    alex.pensize(30)

    # for loop - outer box
    for i in range (4):
        alex.forward(560)
        alex.left(90)

    tess.color("blue")
    tess.speed(100)
    tess.penup()
    tess.setpos(-250, -250)
    tess.pensize(27)
    tess.pendown()
    # for loop - boustrophedon
    def create_boustrophedon():
        for i in range (9):
            tess.forward(500)
            tess.left(90)
            tess.forward(26.1)
            tess.left(90)
            tess.forward(500)
            tess.right(90)
            tess.forward(26.1)
            tess.right(90)

    create_boustrophedon()
    # final line
    tess.forward(500)
    tess.left(90)
    tess.forward(26.1)
    tess.left(90)
    tess.forward(500)
    tess.right(90)

    wn.exitonclick()

main()