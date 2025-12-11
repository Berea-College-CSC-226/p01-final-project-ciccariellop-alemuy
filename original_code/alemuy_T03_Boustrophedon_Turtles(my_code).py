#################################################################################
# Author: Yoseph Alemu
# Username: alemuy
#
# Assignment: Boustrophedon Turtle Drawing
# Purpose: Draw a large square and fill it with a boustrophedon pattern
#################################################################################
# Acknowledgements:
# Thanks to the turtle graphics library and our class videos.
#
#################################################################################
import turtle


def drawsquare(alex):
    for x in range(4):
        alex.speed(6)
        alex.color('purple')
        alex.forward(500)
        alex.left(90)


def drawpattern(alex):
    alex.speed(4)
    alex.forward(452)
    for y in range(9):
        for left in range(1):
            alex.left(90)
            alex.forward(25)
            alex.left(90)
            alex.forward(452)
            for right in range(1):
                alex.right(90)
                alex.forward(25)
                alex.right(90)
                alex.forward(452)
                print(alex.pos())


def setup4box(alex):
    alex.penup()
    alex.hideturtle()
    alex.color('light green')
    alex.goto(-250, -250)
    alex.left(90)
    alex.forward(25)
    alex.right(90)
    alex.forward(25)
    alex.down()
    alex.showturtle()


def add_label(alex):
    """Adds the text label below the drawing."""
    alex.penup()
    alex.goto(0, 0)
    alex.color("Black")
    alex.write("All Clean", align="center", font=("Arial", 28, "bold"))
    alex.pendown()
    alex.hideturtle()


def main():
    wm = turtle.Screen()
    alex = turtle.Turtle()
    alex.pensize(25)
    # set up for drawsquare
    alex.penup()
    alex.hideturtle()
    alex.goto(-250, -250)
    alex.down()
    alex.showturtle()
    # calling functions
    drawsquare(alex)
    setup4box(alex)
    drawpattern(alex)
    add_label(alex)

    wm.exitonclick()


main()


