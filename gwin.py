from graphics import *

win = GraphWin('Test Window')

rct = Rectangle(Point(50,50),Point(150,150))
rct.draw(win)

txt = Text(Point(100,20), "click in the box to quit")
txt.draw(win)

closed = False

while not closed:

    click = win.getMouse()

    if click.x > 50 and click.x < 150:
        if click.y > 50 and click.y < 150:
            closed = True

win.close()
